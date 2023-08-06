# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phylm', 'phylm.clients', 'phylm.sources', 'phylm.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'cinemagoer>=2022.12.4,<2023.0.0',
 'click>=8.0.1,<9.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['phylm = phylm.__main__:main']}

setup_kwargs = {
    'name': 'phylm',
    'version': '6.0.0',
    'description': 'Phylm',
    'long_description': '# Phylm\n\n[![Actions Status](https://github.com/dbatten5/phylm/workflows/Tests/badge.svg)](https://github.com/dbatten5/phylm/actions)\n[![Actions Status](https://github.com/dbatten5/phylm/workflows/Release/badge.svg)](https://github.com/dbatten5/phylm/actions)\n[![codecov](https://codecov.io/gh/dbatten5/phylm/branch/master/graph/badge.svg?token=P233M48EA6)](https://codecov.io/gh/dbatten5/phylm)\n[![PyPI version](https://badge.fury.io/py/phylm.svg)](https://badge.fury.io/py/phylm)\n\nFilm data aggregation with async support.\n\n## Motivation\n\nWhen deciding which film to watch next, it can be helpful to have some key datapoints at\nyour fingertips, for example, the genre, the cast, the Metacritic score and, perhaps\nmost importantly, the runtime. This package provides a Phylm class to gather information\nfrom various sources for a given film.\n\n## Installation\n\n```bash\npip install phylm\n```\n\n## Usage\n\n```python\n>>> import asyncio\n>>> from phylm import Phylm\n>>> p = Phylm("The Matrix")\n>>> asyncio.run(p.load_source("imdb"))\n>>> p.imdb.year\n1999\n>>> p.imdb.rating\n8.7\n```\n\n`phylm` also provides some tools around movie search results and more:\n\n```python\n>>> from phylm.tools import search_movies, get_streaming_providers\n>>> search_movies("the matrix")\n[{\n  \'title\': \'The Matrix\',\n  \'kind\': \'movie\',\n  \'year\': 1999,\n  \'cover_photo\': \'https://some-url.com\',\n  \'imdb_id\': \'0133093\',\n}, {\n  \'title\': \'The Matrix Reloaded\',\n  \'kind\': \'movie\',\n  \'year\': 2003,\n  \'cover_photo\': \'https://some-url.com\',\n  \'imdb_id\': \'0234215\',\n}, {\n...\n>>> get_streaming_providers("0234215", regions=["gb"])\n{\n  \'gb\': {\n    \'rent\': [{\n      \'display_priority\': 8,\n      \'logo_path\': \'/pZgeSWpfvD59x6sY6stT5c6uc2h.jpg\',\n      \'provider_id\': 130,\n      \'provider_name\': \'Sky Store\',\n    }],\n    \'flatrate\': [{\n      \'display_priority\': 8,\n      \'logo_path\': \'/ik9djlxNlex6sY6Kjsundc2h.jpg\',\n      \'provider_id\': 87,\n      \'provider_name\': \'Netflix\',\n    }]\n  }, {\n  ...\n}\n```\n\n## Help\n\nSee the [documentation](https://dbatten5.github.io/phylm) for more details.\n\n## Licence\n\nMIT\n',
    'author': 'Dom Batten',
    'author_email': 'dominic.batten@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dbatten5/phylm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
