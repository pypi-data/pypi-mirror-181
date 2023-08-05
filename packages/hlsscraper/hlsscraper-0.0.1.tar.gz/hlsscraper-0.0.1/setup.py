# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlsscraper', 'hlsscraper.locators', 'hlsscraper.pages']

package_data = \
{'': ['*']}

install_requires = \
['MechanicalSoup>=1.2.0,<2.0.0', 'pandas>=1.5,<2.0']

setup_kwargs = {
    'name': 'hlsscraper',
    'version': '0.0.1',
    'description': '',
    'long_description': '# HLS-scraper\n\nThis project is a webscraper for the [Historical Dictionary of Switzerland (HDS)](https://hls-dhs-dss.ch/).\n\n## Installation\n\n````bash\npip install hlsscraper\n````\n\n## Usage\n\nPlease use the already scraped [hls_base.csv](https://github.com/lemonhead94/HLS-scraper/blob/main/data/hls_base.csv) from 12.12.2022 as basis so only updates and new records need to be fetched.\nThis will help not to stress HLS servers to much.\n\n````python\nimport hlsscraper\n\nhlsscraper.scrape(\n    base_csv_path=f"{os.getcwd()}/data/hls_base.csv",\n    update_csv_path=f"{os.getcwd()}/data/hls_updates.csv",\n    new_csv_path=f"{os.getcwd()}/data/hls_new.csv",\n    last_scraping="12.12.2022",\n    crawl_delay=20,  # as per https://hls-dhs-dss.ch/robots.txt\n)\n````\n\n## Development\n\n```bash\n# download a fresh python 3.9\nconda create -n py39 python=3.9\n# create a .venv inside the project and link against the Python 3.9 version installed through conda\npoetry env use ~/.conda/envs/py39/bin/python\n# install required packages defined in pyproject.toml into .venv\npoetry install\n# set up git hooks for autoformatting and linting (black, isort8, flake8) --> .pre-commit-config.yaml\npre-commit install\n```',
    'author': 'Jorit Studer',
    'author_email': 'jorit.studer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
