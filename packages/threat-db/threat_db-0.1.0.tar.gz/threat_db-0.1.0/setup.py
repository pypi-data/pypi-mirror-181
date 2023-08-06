# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['threat_db']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.2.2,<3.0.0',
 'gql[all]>=3.4.0,<4.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'orjson>=3.8.3,<4.0.0',
 'packageurl-python>=0.10.4,<0.11.0',
 'protobuf==3.20.1',
 'pydgraph>=21.3.2,<22.0.0',
 'rich>=12.6.0,<13.0.0',
 'uwsgi>=2.0.21,<3.0.0']

entry_points = \
{'console_scripts': ['threat_db = threat_db.cli:main']}

setup_kwargs = {
    'name': 'threat-db',
    'version': '0.1.0',
    'description': 'A graphql server for vulnerabilities powered by dgraph',
    'long_description': "# Introduction\n\n## Development setup\n\n```\ngit clone <repo>\ncd threat-db\nmkdir -p $HOME/dgraph $HOME/threatdb_data_dir\ndocker compose up\n```\n\nThis would start a minimal api and an instance of [dgraph](https://dgraph.io) standalone.\n\n## Create schemas\n\nTo explicitly create the schemas prior to importing data\n\n```\ngit clone <repo>\npoetry install\nthreat_db --init --dgraph-host localhost:9080 --graphql-host http://localhost:8080\n```\n\nSchema creation is automatic when the api runs from docker compose.\n\n## Import data\n\n```\nthreat_db --data-dir\n```\n\nWhen invoked with docker compose, any json file present in the directory `THREATDB_DATA_DIR` would be imported automatically.\n\n## Rest API\n\n### Healthcheck\n\n```\ncurl http://0.0.0.0:9000/healthcheck\n```\n\n### Import data\n\n```\ncurl -F 'file=@/tmp/bom.json' http://0.0.0.0:9000/import\n```\n",
    'author': 'Team ngcloudsec',
    'author_email': 'cloud@ngcloud.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
