# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosu',
 'aiosu.classes',
 'aiosu.classes.legacy',
 'aiosu.utils',
 'aiosu.v1',
 'aiosu.v2']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'aiolimiter>=1.0.0,<2.0.0',
 'emojiflags>=0.1.1,<0.2.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0']

extras_require = \
{'docs': ['toml>=0.10.2,<0.11.0',
          'sphinx>=5.3.0,<6.0.0',
          'sphinx-rtd-theme>=1.1.1,<2.0.0'],
 'test': ['pytest>=7.2.0,<8.0.0',
          'pytest-asyncio>=0.20.2,<0.21.0',
          'pytest-mock>=3.10.0,<4.0.0',
          'toml>=0.10.2,<0.11.0',
          'types-toml>=0.10.8.1,<0.11.0.0']}

setup_kwargs = {
    'name': 'aiosu',
    'version': '0.1.3',
    'description': 'Simple and fast osu! API v1 and v2 library',
    'long_description': 'aiosu\n=====\n\n|Python| |pypi| |pre-commit.ci status| |rtd| |pytest| |mypy|\n\nSimple and fast osu! API v1 and v2 library\n\n\nFeatures\n--------\n\n- Support for API v1 and API v2\n- Rate limit handling\n- Utilities for osu! related calculations\n- Easy to use\n\n\nInstalling\n----------\n\n**Python 3.9 or higher is required**\n\nTo install the library, simply run the following commands\n\n.. code:: sh\n\n    # Linux/macOS\n    python3 -m pip install -U aiosu\n\n    # Windows\n    py -3 -m pip install -U aiosu\n\nTo install the development version, do the following:\n\n.. code:: sh\n\n    $ git clone https://github.com/NiceAesth/aiosu\n    $ cd aiosu\n    $ python3 -m pip install -U .\n\n\nAPI v1 Example\n--------------\n\n.. code:: py\n\n   import aiosu\n   import asyncio\n\n\n   async def main():\n       # async with syntax\n       async with aiosu.v1.Client("osu api token") as client:\n           user = await client.get_user(7782553)\n\n       # regular syntax\n       client = aiosu.v1.Client("osu api token")\n       user = await client.get_user(7782553)\n       client.close()\n\n\n   if __name__ == "__main__":\n       asyncio.run(main())\n\n\nAPI v2 Example\n--------------\n\n.. code:: py\n\n    import aiosu\n    import asyncio\n    import datetime\n\n\n    async def main():\n        token = aiosu.classes.OAuthToken.parse_obj(json_token_from_api)\n\n        # or\n\n        token = aiosu.classes.OAuthToken(\n            access_token="access token",\n            refresh_token="refresh token",\n            expires_on=datetime.datetime.utcnow()\n            + datetime.timedelta(days=1),  # can also be string\n        )\n\n        # async with syntax\n        async with aiosu.v2.Client(\n            client_secret="secret", client_id=1000, token=token\n        ) as client:\n            user = await client.get_me()\n\n        # regular syntax\n        client = aiosu.v2.Client(client_secret="secret", client_id=1000, token=token)\n        user = await client.get_me()\n        client.close()\n\n\n    if __name__ == "__main__":\n        asyncio.run(main())\n\n\nYou can find more examples in the examples directory.\n\n\nContributing\n------------\n\nPlease read the `CONTRIBUTING.rst <.github/CONTRIBUTING.rst>`__ to learn how to contribute to aiosu!\n\n\nAcknowledgments\n---------------\n\n-  `discord.py <https://github.com/Rapptz/discord.py>`__\n   for README formatting\n-  `osu!Akatsuki <https://github.com/osuAkatsuki/performance-calculator>`__\n   for performance and accuracy utils\n\n\n.. |Python| image:: https://img.shields.io/pypi/pyversions/aiosu.svg\n    :target: https://pypi.python.org/pypi/aiosu\n    :alt: Python version info\n.. |pypi| image:: https://img.shields.io/pypi/v/aiosu.svg\n    :target: https://pypi.python.org/pypi/aiosu\n    :alt: PyPI version info\n.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/NiceAesth/aiosu/master.svg\n    :target: https://results.pre-commit.ci/latest/github/NiceAesth/aiosu/master\n    :alt: pre-commit.ci status\n.. |pytest| image:: https://github.com/NiceAesth/aiosu/actions/workflows/pytest.yml/badge.svg\n    :target: https://github.com/NiceAesth/aiosu/actions/workflows/pytest.yml\n    :alt: pytest Status\n.. |mypy| image:: https://github.com/NiceAesth/aiosu/actions/workflows/mypy.yml/badge.svg\n    :target: https://github.com/NiceAesth/aiosu/actions/workflows/mypy.yml\n    :alt: mypy Status\n.. |rtd| image:: https://readthedocs.org/projects/aiosu/badge/?version=latest\n    :target: https://aiosu.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n',
    'author': 'Nice Aesthetics',
    'author_email': 'nice@aesth.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NiceAesth/aiosu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
