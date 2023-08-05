# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['here_transit']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'async-timeout>=4.0.2,<5.0.0', 'yarl>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'here-transit',
    'version': '1.2.0',
    'description': 'Asynchronous Python client for the HERE Transit V8 API',
    'long_description': '# here_transit\n\nAsynchronous Python client for the HERE Transit V8 API\n\n[![GitHub Actions](https://github.com/eifinger/here_transit/workflows/CI/badge.svg)](https://github.com/eifinger/here_transit/actions?workflow=CI)\n[![PyPi](https://img.shields.io/pypi/v/here_transit.svg)](https://pypi.python.org/pypi/here_transit)\n[![PyPi](https://img.shields.io/pypi/l/here_transit.svg)](https://github.com/eifinger/here_transit/blob/master/LICENSE)\n[![codecov](https://codecov.io/gh/eifinger/here_transit/branch/master/graph/badge.svg)](https://codecov.io/gh/eifinger/here_transit)\n[![Downloads](https://pepy.tech/badge/here_transit)](https://pepy.tech/project/here_transit)\n\n## Installation\n\n```bash\npip install here_transit\n```\n\n## Usage\n\n```python\nimport asyncio\n\nfrom here_transit import HERETransitApi, Place, Return\n\nAPI_KEY = "<YOUR_API_KEY>"\n\n\nasync def main() -> None:\n    """Show example how to get location of your tracker."""\n    async with HERETransitApi(api_key=API_KEY) as here_transit:\n        response = await here_transit.route(\n            origin=Place(latitude=50.12778680095556, longitude=8.582081794738771),\n            destination=Place(latitude=50.060940891421765, longitude=8.336477279663088),\n            return_values=[Return.TRAVEL_SUMMARY],\n        )\n        print(\n            f"Duration is: {response[\'routes\'][0][\'sections\'][0][\'travelSummary\'][\'duration\']}"\n        )\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n',
    'author': 'Kevin Stillhammer',
    'author_email': 'kevin.stillhammer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/eifinger/here_transit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
