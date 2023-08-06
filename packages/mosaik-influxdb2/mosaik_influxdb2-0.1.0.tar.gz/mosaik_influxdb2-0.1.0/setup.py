# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mosaik', 'mosaik.influxdb2']

package_data = \
{'': ['*']}

install_requires = \
['influxdb-client>=1.35.0,<2.0.0',
 'mosaik-api>=3.0.3,<4.0.0',
 'numpy>=1.23.5,<2.0.0']

setup_kwargs = {
    'name': 'mosaik-influxdb2',
    'version': '0.1.0',
    'description': 'An adapter to connect mosaik with InfluxDB 2',
    'long_description': '# mosaik-influxdb2\n\n## Description\nThis package contains an adapter to write data from a mosaik simulation into an\nInfluxDB 2 database.\n\n## Usage\n\nTo use the simulator, first add it to your `sim_config`:\n\n```python\nsim_config = {\n    "InfluxWriter": {"python": "mosaik.influxdb2.writer:Simulator"},\n    # ...\n}\n```\n\nNext, you need to start the simulator. Here, you have two choices to make:\n\n1. The simulator can run both in time-based mode with a fixed step size or in\n   event-based mode without a step size. You can choose the time-based mode by giving\n   the parameter `step_size` when starting the simulator. If you give `step_size=None`\n   (or don’t specify anything), the simulator will use the event-based mode.\n2. You can either supply a start date (as a string parseable by Python’s `datetime`\n   module) which will be combined with the (mosaik) time and time resolution to\n   calculate each step’s time, or you can supply the time for each step on the\n   `local_time` attribute (again, as a string). If you give both, the value on the\n   `local_time` attribute will take precedence.\n\nSo one possible invocation would be\n\n```python\ninflux_sim = world.start("InfluxWriter",\n    step_size=900,\n    start_date="2022-01-01 00:00:00Z",\n)\n```\n\nto start the simulator in time-based mode with a step size of 900 and times based on\nthe given start date. You can leave off either argument with the effects described\nabove.\n\nFinally, the model needs to be started with your Influx credentials:\n\n```python\ninflux = influx_sim.Database(\n    url="http://localhost:8086",\n    org=\'.\',\n    bucket=\'my_bucket\',\n    token=\'secret_token\',\n    measurement=\'experiment_0001\'\n)\n```\n\nWe recommend setting a new value for the measurement on each simulation run. (For\nexample, you can use the start time of your simulation or a random UUID.)\n\nAfterwards, you can define `world.connect(other_entity, influx, attrs)` as you like.\n\nThe simulator supports only one instance of the Database model. If you want to connect\nto several databases, you will need to start several instances of the simulator as well.\n',
    'author': 'Eike Schulte',
    'author_email': 'eike.schulte@offis.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
