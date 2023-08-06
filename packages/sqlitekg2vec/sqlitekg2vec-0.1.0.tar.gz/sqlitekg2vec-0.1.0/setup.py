# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlitekg2vec']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'cachetools>=4.2,<5',
 'gensim>=4.0.1,<5.0.0',
 'nest_asyncio>=1.5.4,<2.0.0',
 'pyrdf2vec>=0.2.3',
 'rdflib>=6.1.1,<7.0.0']

setup_kwargs = {
    'name': 'sqlitekg2vec',
    'version': '0.1.0',
    'description': 'SQLiteKG implements the KG class from pyRDF2Vec by using a local SQLite database for storing and querying a KG.',
    'long_description': "# sqlitekg2vec\n\nsqlitekg2vec is an extension of\n[pyRDF2Vec](https://github.com/IBCNServices/pyRDF2Vec), which is a popular\nlibrary to train RDF2Vec models for RDF-based knowledge graphs. It aims to be\nless memory hungry than building KGs from scratch using pyRDF2Vec, or running a\nlocal/remote triplestore.\n\n\nsqlitekg2vec creates a local SQLite database with a single big table for all the\nstatements of a knowledge graph, and an additional table as an index of KG\nentity names to integer IDs. This SQLite database will be referenced as SQLite\nKG in the remaining documentation.\n\n## Usage\n\n```python\nimport sqlitekg2vec\n\nfrom pyrdf2vec import RDF2VecTransformer\nfrom pyrdf2vec.embedders import Word2Vec\nfrom pyrdf2vec.walkers import RandomWalker\n\nwith sqlitekg2vec.open_from_pykeen_dataset('dbpedia50', combined=True) as kg:\n    transformer = RDF2VecTransformer(\n        Word2Vec(epochs=100),\n        walkers=[RandomWalker(max_walks=200,\n                              max_depth=4,\n                              random_state=133,\n                              with_reverse=False,\n                              n_jobs=4)],\n        verbose=1\n    )\n    # train RDF2Vec\n    ent = kg.entities()\n    embeddings, _ = transformer.fit_transform(kg, ent)\n    print(kg.pack(ent, embeddings))\n```\n\n### Create from PyKeen dataset\n\n[PyKeen](https://github.com/pykeen/pykeen) is a popular library for knowledge\ngraph embeddings, and it specifies a number of datasets that are commonly\nreferenced in scientific literature. An SQLite KG can be constructed from a\nPyKeen dataset by specifying the name of the dataset or passing the dataset\ninstance.\n\nIn the following code snippet, the `db100k` dataset, which is a subsampling of\nDBpedia, is used to construct an SQLite KG.\n\n```python\nimport sqlitekg2vec\n\nwith sqlitekg2vec.open_from_pykeen_dataset('db100k', combined=True) as kg:\n    # ...\n    pass\n```\n\n**Parameters:**\n\n* *combined* - `False` if only the training set of a dataset shall be used for\n  the training of RDF2Vec. `True` if all the sets (training, testing and\n  validation) shall be used. It is `False` by default.\n\n### Create from TSV file\n\nIn order to save memory for big knowledge graphs, it might be a good idea to\nload the statements of such a knowledge graph from a TSV file into a SQLite KG.\nAll the rows in the TSV file must have three columns, where the first column is\nthe subject, the second is the predicate, and the last column is the object.\n\nThe following code snippet creates a new SQLite KG instance from the statements\nof the specified TSV file, which has been compressed using GZIP.\n\n```python\nimport sqlitekg2vec\n\nwith sqlitekg2vec.open_from_tsv_file('statements.tsv.gz',\n                                     compression='gzip') as kg:\n    # ...\n    pass\n```\n\n**Parameters:**\n\n* *skip_header* - `True` if the first row shall be skipped, because it is a\n  header row for example. `False` if it shouldn't be skipped. It is `False` by\n  default.\n* *compression* - specifies the compression type of source TSV file. The default\n  value is `None`, which means that the source isn't compressed. At the moment,\n  only `'gzip'` is supported as compression type.\n\n### Create from Pandas dataframe\n\nA knowledge graph can be represented in a Pandas dataframe, and this method\nallows to create an SQLite KG from a dataframe. While the dataframe can have\nmore than three columns, the three columns representing the subject, predicate\nand object must be specified in this particular order.\n\nThe following code snippet creates a new SQLite KG instance from a dataframe.\n\n```python\nimport sqlitekg2vec\n\nwith sqlitekg2vec.open_from_dataframe(df, column_names=(\n        'subj', 'pred', 'obj')) as kg:\n    # ...\n    pass\n```\n\n**Parameters:**\n\n* *column_names* - a tuple of three indices for the dataframe, which can be an\n  integer or string. The first entry of the tuple shall point to the subject,\n  the second to the predicate, and the third one to the object. `(0, 1, 2)` are\n  the default indices.\n\n## Contact\n\n* Kevin Haller - [contact@kevinhaller.dev](mailto:contact@kevinhaller.dev)",
    'author': 'Kevin Haller',
    'author_email': 'contact@kevinhaller.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/khaller93/sqlitekg2vec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
