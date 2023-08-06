# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kafka_connect']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.25,<3.0']

entry_points = \
{'console_scripts': ['kafka-connect = kafka_connect.cli:cli',
                     'kc = kafka_connect.cli:cli']}

setup_kwargs = {
    'name': 'kafka-connect-py',
    'version': '0.2.3',
    'description': 'A client for the Confluent Platform Kafka Connect REST API.',
    'long_description': '# Kafka Connect Python\n\nThe Kafka Connect REST API allows you to manage connectors that move data between Apache Kafka and other systems.\n\nThe `kc` command line tool provides commands for getting information about the Kafka Connect cluster and its connectors, creating new connectors, updating existing connectors, deleting connectors, etc.\n\nThis project aims to supported all features of the [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html#kconnect-rest-interface).\n\n## Install\n\n```bash\npip install kafka-connect-py\n```\n\n## Command Line Usage\n\nRetrieve the version and other details of the Kafka Connect cluster.\n\n```bash\n$ kc get-cluster\n```\n\nRetrieve the details of a single connector.\n\n```bash\n$ kc get-connector <connector>\n```\n\nRetrieve a list of active connectors. The `--expand\' option can be used to retrieve additional information about the connectors, such as their status or metadata.\n\n```bash\n$ kc get-connectors [--expand=status|info]\n```\n\nCreate a new connector using the configuration specified in the given file. If the connector already exists or a rebalance is in process, Wil return a status code of 409.\n\n```bash\n$ kc create-connector <config_file>\n```\n\nUpdate the configuration for an existing connector. If a rebalance is in process, Wil return a status code of 409.\n\n```bash\n$ kc update-connector <connector> <config_file>\n```\n\nRetrieve the configuration of a connector.\n\n```bash\n$ kc get-connector <connector>\n```\n\nRetrieve the config of a connector.\n\n```bash\n$ kc get-connector-config <connector>\n```\n\nRetrieve the status of a connector.\n\n```bash\n$ kc get-connector-status <connector>\n```\n\nRetrieve the tasks of a connector. The `--include-tasks\' option can be used to include task information in the response.\n\n```bash\n$ kc get-connector-tasks <connector> [--include-tasks]\n```\n\nPause a connector.\n\n```bash\n$ kc pause-connector <connector>\n```\n\nResume a connector that was previously paused.\n\n```bash\n$ kc resume-connector <connector>\n```\n\nDelete a connector.\n\n```bash\n$ kc delete-connector <connector>\n```\n\nValidate the configuration specified in the given file. If the configuration is valid, Wil return a status code of 200.\n\n```bash\n$ kc validate-connector-config <config_file>\n```\n\nRetrieve metadata about the specified connector plugin.\n\n```bash\n$ kc get-connector-plugin <connector>\n```\n\nRetrieve metadata about all available connector plugins.\n\n```bash\n$ kc get-connector-plugins\n```\n\n\n### Python\n\n```python\n# Import the class\nfrom kafka_connect import KafkaConnect\n\n# Instantiate the client\nclient = KafkaConnect(endpoint="http://localhost:8083")\n\n# Get the version and other details of the Kafka Connect cluster\ncluster = client.get_cluster()\nprint(cluster)\n\n# Get a list of active connectors\nconnectors = client.get_connectors()\nprint(connectors)\n\n# Create a new connector\nconfig = {\n    "name": "my-connector",\n    "config": {\n        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",\n        "tasks.max": "1",\n        "connection.url": "jdbc:postgresql://localhost:5432/mydatabase",\n        "connection.user": "myuser",\n        "connection.password": "mypassword",\n        "table.whitelist": "mytable",\n        "mode": "timestamp+incrementing",\n        "timestamp.column.name": "modified_at",\n        "validate.non.null": "false",\n        "incrementing.column.name": "id",\n        "topic.prefix": "my-connector-",\n    },\n}\nresponse = client.create_connector(config)\nprint(response)\n\n# Update an existing connector\nnew_config = {\n    "config": {\n        "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",\n        "tasks.max": "1",\n        "connection.url": "jdbc:postgresql://localhost:5432/mydatabase",\n        "connection.user": "myuser",\n        "connection.password": "mypassword",\n        "table.whitelist": "mytable",\n        "mode": "timestamp+incrementing",\n        "timestamp.column.name": "modified_at",\n        "validate.non.null": "false",\n        "incrementing.column.name": "id",\n        "topic.prefix": "my-connector-",\n    },\n}\nresponse = client.update_connector("my-connector", new_config)\nprint(response)\n\n# Restart a connector\nresponse = client.restart_connector("my-connector")\nprint(response)\n\n# Delete a connector\nresponse = client.delete_connector("my-connector")\nprint(response)\n```\n\n## Tests\n\n```\npython3 -m unittest tests/test_kafka_connect.py -v\n```',
    'author': 'Aidan Melen',
    'author_email': 'aidan-melen@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
