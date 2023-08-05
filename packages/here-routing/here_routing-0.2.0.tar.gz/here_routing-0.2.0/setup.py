# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['here_routing']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'async-timeout>=4.0.2,<5.0.0', 'yarl>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'here-routing',
    'version': '0.2.0',
    'description': 'Asynchronous Python client for the HERE Routing V8 API',
    'long_description': '# here_routing\n\nAsynchronous Python client for the HERE Routing V8 API\n\n[![GitHub Actions](https://github.com/eifinger/here_routing/workflows/CI/badge.svg)](https://github.com/eifinger/here_routing/actions?workflow=CI)\n[![PyPi](https://img.shields.io/pypi/v/here_routing.svg)](https://pypi.python.org/pypi/here_routing)\n[![PyPi](https://img.shields.io/pypi/l/here_routing.svg)](https://github.com/eifinger/here_routing/blob/master/LICENSE)\n[![codecov](https://codecov.io/gh/eifinger/here_routing/branch/master/graph/badge.svg)](https://codecov.io/gh/eifinger/here_routing)\n[![Downloads](https://pepy.tech/badge/here_routing)](https://pepy.tech/project/here_routing)\n\n## Installation\n\n```bash\npip install here_routing\n```\n\n## Usage\n\n```python\nimport asyncio\n\nfrom here_routing import HERERoutingApi, Place, Return, TransportMode\n\nAPI_KEY = "<YOUR_API_KEY>"\n\n\nasync def main() -> None:\n    """Show example how to get duration of your route."""\n    async with HERERoutingApi(api_key=API_KEY) as here_routing:\n        response = await here_routing.route(\n            transport_mode=TransportMode.CAR,\n            origin=Place(latitude=50.12778680095556, longitude=8.582081794738771),\n            destination=Place(latitude=50.060940891421765, longitude=8.336477279663088),\n            return_values=[Return.SUMMARY],\n        )\n        print(\n            f"Duration is: {response[\'routes\'][0][\'sections\'][0][\'summary\'][\'duration\']}"\n        )\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n',
    'author': 'Kevin Stillhammer',
    'author_email': 'kevin.stillhammer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/eifinger/here_routing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
