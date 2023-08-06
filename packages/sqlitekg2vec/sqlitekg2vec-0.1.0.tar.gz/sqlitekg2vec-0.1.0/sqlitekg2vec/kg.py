import logging
import operator
from functools import partial
from os import remove
from os.path import exists
from sqlite3 import connect, Connection
from typing import Iterable, Tuple, List, Set, Any, Sequence, Union

from cachetools import cachedmethod, FIFOCache
from cachetools.keys import hashkey
from pyrdf2vec.typings import Hop, Literals, Entities, Embeddings
from pyrdf2vec.graphs import Vertex

EntityName = str
EntityNames = List[EntityName]
EntityID = Union[int, str]
EntityIDs = List[EntityID]
Triple = Tuple[EntityName, EntityName, EntityName]


class _Importer:
    """ importer of KG into the SQLite database """

    def __init__(self, con: Connection,
                 skip_predicates: Set[EntityName] = None):
        """ creates a new importer using the given connection. This importer
        allows to import the triples of a KG.

        :param con: connection which shall be used for the import.
        :param skip_predicates: a set of predicates, which makes all the
        statements with one of these predicates to be ignored.
        """
        self._con = con
        self._skip_predicates = skip_predicates \
            if skip_predicates is not None else set([])
        self._cursor = con.cursor()
        self._entity_map = {}

    def _create_schema(self) -> None:
        """ creates the basic schema of the SQLite database. """
        self._cursor.execute('''
CREATE TABLE resource(
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    iri NOT NULL UNIQUE
);      ''')
        self._cursor.execute('''
CREATE TABLE statement(
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    subj INTEGER NOT NULL,
    pred INTEGER NOT NULL,
    obj INTEGER NOT NULL,
    FOREIGN KEY (subj) REFERENCES resource (resource_id),
    FOREIGN KEY (pred) REFERENCES resource (resource_id),
    FOREIGN KEY (obj) REFERENCES resource (resource_id),
    UNIQUE(subj,pred,obj)
);      ''')

    def _insert_entity(self, entity: EntityName) -> int:
        """ inserts the given entity into the database, if it doesn't already
        exist. This method returns the ID of this entity regardless of whether
        the entity was newly inserted or it already existed.

        :param entity: name of the entity that shall be inserted.
        :return: the unique integer ID of the given entity.
        """
        if entity in self._entity_map:
            return self._entity_map[entity]
        else:
            self._cursor.execute('INSERT INTO resource (iri) VALUES (?);',
                                 (entity,))
            key = self._cursor.execute('SELECT last_insert_rowid();') \
                .fetchone()[0]
            self._entity_map[entity] = int(key)
            return key

    def import_kg(self, data: Iterable[Tuple[str, str, str]]) -> None:
        """ inserts all the statements into the database.

        :param data: a sequence of statements that shall be imported.
        """
        for subj, pred, obj in data:
            if pred in self._skip_predicates:
                continue
            subj_key = self._insert_entity(subj)
            pred_key = self._insert_entity(pred)
            obj_key = self._insert_entity(obj)
            self._cursor.execute('INSERT INTO statement (subj, pred, obj) '
                                 'VALUES (?, ?, ?);',
                                 (subj_key, pred_key, obj_key))

    def __enter__(self):
        self._create_schema()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self._con is not None:
                self._con.commit()
        self._entity_map = None


class _QueryManager:
    """ this class maintains SQL queries """

    entity_id_query = 'SELECT resource_id FROM resource WHERE iri = ?;'

    entity_name_query = 'SELECT iri FROM resource WHERE resource_id = ?;'

    entities_count_query = '''
SELECT count(*)
FROM (SELECT subj as id FROM statement UNION SELECT obj as id FROM statement);
'''

    predicates_count_query = 'SELECT count(distinct pred) FROM statement;'

    statements_count_query = 'SELECT count(*) FROM statement;'

    all_entities_query = '''
SELECT id, iri
FROM (SELECT subj as id FROM statement UNION
      SELECT obj as id FROM statement) entity
JOIN resource ON entity.id = resource.resource_id;
'''

    hops_query = {
        'forward': 'SELECT pred, obj FROM statement WHERE subj = ?;',
        'backward': 'SELECT pred, subj FROM statement WHERE obj = ?;',
    }


class SQLiteKG:
    """ represents a Knowledge Graph persisted in a SQLite database """

    def __init__(self, data: Iterable[Triple],
                 *,
                 skip_verify: bool = False,
                 skip_predicates: Iterable[str] = None,
                 cache_size: int = 4096,
                 db_file_path: str = 'tmp.db'):
        """ creates a new SQLite KG for the given data. The database is
        persisted in the specified file path.

        :param data: an iterable stream of triples.
        :param skip_verify: `False`, if it shall be checked whether the
        specified list of entities (for training) are actually part of this
        knowledge graph. Otherwise, it is `True`. It is `False` by default.
        :param skip_predicates: a list of predicates, which makes all the
        statements with one of these predicates to be ignored.
        :param cache_size: size of the cache. It holds 4096 entries by default.
        :param db_file_path: path to the file that shall hold the KG on disk.
        """
        self._data = data
        self.skip_verify = skip_verify
        self._skip_predicates = set(skip_predicates) \
            if skip_predicates is not None else set([])
        self._db_file_path = db_file_path
        self._cache = FIFOCache(maxsize=cache_size)
        self._con: Connection

    @property
    def _is_remote(self) -> bool:
        return False

    @property
    def entity_count(self) -> int:
        """ count of entities (occur as subject or object) in this KG. """
        cursor = self._con.cursor()
        try:
            return int(cursor.execute(_QueryManager.entities_count_query)
                       .fetchone()[0])
        finally:
            cursor.close()

    @property
    def predicate_count(self) -> int:
        """ count of distinct predicates in the KG. """
        cursor = self._con.cursor()
        try:
            return int(cursor.execute(_QueryManager.predicates_count_query)
                       .fetchone()[0])
        finally:
            cursor.close()

    @property
    def statement_count(self) -> int:
        """ count of statements in the KG. """
        cursor = self._con.cursor()
        try:
            return int(cursor.execute(_QueryManager.statements_count_query)
                       .fetchone()[0])
        finally:
            cursor.close()

    def id(self, entity_name: EntityName) -> Union[EntityID, None]:
        """ returns the integer ID of the entity in form of a string.

        :param entity_name: name of the entity for which to get the ID.
        :return: the integer ID of the entity in form of a string, or `None`,
        if no entity with such a name could be found.
        """
        cursor = self._con.cursor()
        try:
            result = cursor.execute(_QueryManager.entity_id_query,
                                    (entity_name,))
            entity_id_tp = result.fetchone()
            return None if entity_id_tp is None else str(entity_id_tp[0])
        finally:
            cursor.close()

    def from_id(self, entity_id: EntityID) -> Union[EntityName, None]:
        """ returns the name of the entity in form of a string.

        :param entity_id: ID of the entity for which to get the name.
        :return: the integer ID of the entity in form of a string, or `None`, if
        no entity with such a ID could be found.
        """
        cursor = self._con.cursor()
        try:
            result = cursor.execute(_QueryManager.entity_name_query,
                                    (int(entity_id),))
            entity_name_tp = result.fetchone()
            return None if entity_name_tp is None else entity_name_tp[0]
        finally:
            cursor.close()

    def entities(self, restricted_to: EntityNames = None) -> EntityIDs:
        """ returns all the entities, which occur as either a subject or object
        in a statement of the KG. No entity will be returned twice.

        :param restricted_to: the names (e.g. IRI) of the resources that shall
        be exclusively considered. If `None`, then all entities will be
        returned. It is `None` by default.
        :return: a list with all entity IDs.
        """
        cursor = self._con.cursor()
        try:
            result = cursor.execute(_QueryManager.all_entities_query)
            entities = [(str(row[0]), str(row[1])) for row in result]
            if restricted_to is None:
                return [e[0] for e in entities]
            else:
                restriction = set(restricted_to)
                return [e[0] for e in entities if e[1] in restriction]
        finally:
            cursor.close()

    def pack(self, entities: EntityIDs,
             embeddings: Embeddings) -> Sequence[Tuple[EntityName, str]]:
        """ packs the entities with their embeddings.

        :param entities: IDs of the entities with which the embeddings shall be
        packed.
        :param embeddings: which shall be packed with the name of the entity.
        :return: a list of the embeddings with the corresponding name of the
        entity.
        """
        if len(entities) != len(embeddings):
            raise ValueError('list of entities must be the same size as list '
                             'of embeddings')
        cursor = self._con.cursor()
        try:
            result = cursor.execute(_QueryManager.all_entities_query)
            entity_map = {int(row[0]): str(row[1]) for row in result}
            return [(entity_map[int(entityID)], embedding) for
                    entityID, embedding in zip(entities, embeddings)]
        finally:
            cursor.close()

    @staticmethod
    def _parse_hops(vertex: Vertex,
                    result: Iterable[Tuple[Any, Any]],
                    is_reverse: bool = False) -> Iterable['Hop']:
        """ parses the results from the SQL query that is fetching the direct
        hops for the specified vertex.

        :param vertex: for which the query result was returned.
        :param result: the result of the forward or backward query.
        :param is_reverse: If `True`, this function assumes that the result of
        the backward query was passed, otherwise the forward result, if `False`.
        It is `False` by default.
        :return: the extracted direct hops in proper format.
        """
        for row in result:
            other_vertex = Vertex(name=str(row[1]))
            pred = Vertex(name=str(row[0]),
                          vprev=other_vertex if is_reverse else vertex,
                          vnext=vertex if is_reverse else other_vertex,
                          predicate=True)
            yield pred, other_vertex

    @cachedmethod(
        operator.attrgetter("_cache"), key=partial(hashkey, "get_hops")
    )
    def get_hops(self, vertex: 'Vertex',
                 is_reverse: bool = False) -> List['Hop']:
        """ gets the direct hops of specified vertex as a list.

        :param vertex: name of the vertex for which to get the hops.
        :param is_reverse: If `True`, this function gets the parent nodes of a
        vertex (backward links). Otherwise, get the child nodes for this
        vertex (forward links). It is `False` by default.
        :return: the hops of a vertex in (predicate, object) form.
        """
        cursor = self._con.cursor()
        try:
            link_type = 'backward' if is_reverse else 'forward'
            query = _QueryManager.hops_query[link_type]
            result = cursor.execute(query, (int(vertex.name),))
            hops = [hop for hop in self._parse_hops(vertex, result,
                                                    is_reverse)]
            logging.debug('Detected %d (%s) hops for vertex "%s"',
                          len(hops), link_type, vertex.name)
            return hops
        finally:
            cursor.close()

    def get_neighbors(self, vertex: Vertex,
                      is_reverse: bool = False) -> Set[Vertex]:
        """ gets the children or parents neighbors of a vertex.

        :param vertex: name of the vertex for which to get the neighbours.
        :param is_reverse: If `True`, this function gets the parent neighbours
        of a vertex (backward links). Otherwise, get the child neighbours for
        this vertex (forward links). It is `False` by default.
        :return: children or parents neighbors of a vertex.
        """
        cursor = self._con.cursor()
        try:
            link_type = 'backward' if is_reverse else 'forward'
            query = _QueryManager.hops_query[link_type]
            result = cursor.execute(query, (int(vertex.name),))
            return set([pred for pred, _ in self._parse_hops(vertex,
                                                             result,
                                                             is_reverse)])
        finally:
            cursor.close()

    def get_literals(self, entities: EntityIDs, verbose: int = 0) -> Literals:
        """ gets the literals for one or more entities for all the predicates
        chain.

        :param entities: entity or entities for which to get the literals.
        :param verbose: specifies the verbosity level. `0` does not display
        anything; `1` display of the progress of extraction and training of
        walks; `2` debugging. It is `0` by default.
        :return: list that contains literals for each entity.
        """
        logging.warning('SQLite KG doesn\'t support literals')
        return []

    def is_exist(self, entities: EntityIDs) -> bool:
        """ checks whether all provided entities exist in the KG.

        :param entities: IDs of the entities for which to check the existence.
        :return: `True`, if all the entities exists, `False` otherwise.
        """
        ent_in_kg = set([int(x) for x in self.entities()])
        for entity in entities:
            if int(entity) not in ent_in_kg:
                return False
        return True

    def __enter__(self):
        # remove db file if it exists
        if exists(self._db_file_path):
            remove(self._db_file_path)
        # import the KG
        self._con = connect(self._db_file_path)
        logging.info('Importing statements into SQLite KG  with {'
                     'skip_predicates: %s}, stored at the file "%s"'
                     % (self._db_file_path, [x for x in self._skip_predicates]))
        with _Importer(self._con,
                       skip_predicates=self._skip_predicates) as importer:
            importer.import_kg(self._data)
        logging.info('Imported KG with {entities:%d, predicates:%d, '
                     'statements: %d}' % (self.entity_count,
                                          self.predicate_count,
                                          self.statement_count))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._con.close()
        if exists(self._db_file_path):
            remove(self._db_file_path)
