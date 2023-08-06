# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cointainer_scraper_ecb']

package_data = \
{'': ['*'], 'cointainer_scraper_ecb': ['data/*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'dateparser>=1.1.0,<2.0.0',
 'pycountry>=22.3.5,<23.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'cointainer-scraper-ecb',
    'version': '0.1.1',
    'description': 'Cointainer component for scraping coins from the ECB Website.',
    'long_description': '<img src="https://github.com/cointainer/scraper-ecb/raw/main/docs/images/Cointainer-Scraper.png" width="100%" alt="Cointainer-Scraper Banner">\n\n> Cointainer component for scraping coins from the ECB Website.\n\n<div align="center">\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</a>\n<a href="https://github.com/cointainer/cointainer-scraper-ecb/blob/main/LICENSE">\n    <img alt="License" src="https://img.shields.io/github/license/cointainer/\ncointainer-scraper-ecb.svg?color=blue">\n</a><br>\n<a href="https://github.com/cointainer/scraper-ecb"><img src="https://img.shields.io/pypi/pyversions/cointainer-scraper-ecb.svg"></a>\n<a href="">\n  <img src="https://img.shields.io/pypi/v/cointainer-scraper-ecb?color=dar-green" />\n</a>\n</div>\n\n## Introduction\n\nCointainer Scraper (ECB) is one of the components of the Cointainer. This component offers the functionality of scraping euro coin data from the ECB website.\n\nCurrently supported coins:\n- €2 commemorative coins\n  - Country\n  - Feature\n  - Description\n  - Issuing Volume\n  - Issuing Date\n  - Image URLs\n\n## Installation\n\n```bash\npip install cointainer-scraper-ecb\n```\n\n## Example\n```python\nfrom cointainer_scraper_ecb import get_two_euro_commemorative_coins\n\nget_two_euro_commemorative_coins(\n    language="en",\n    year=2004\n)\n```\n> Tested with Python 3.9.13 and cointainer_scraper_ecb v0.1.0 ✔️\n\nTwo data classes are relevant which are beeing returned by the function:\n```python\ndef get_two_euro_commemorative_coins(\n    lang: str = "en",\n    year: int = START_YEAR\n) -> List[TwoEuro]: ...\n```\n\n```python\n@dataclass\nclass Coinage:\n    """Represents a coin of a country to be collected."""\n\n    country: Optional[str]\n    image_default_url: Optional[str]\n    volume: Optional[int]\n    image_default_url_info: Optional[str] = None\n    country_info: Optional[str] = None\n    circulation_date: Optional[datetime.date] = None\n    image_attribution: Optional[str] = None\n    circulation_date_info: Optional[str] = None\n    volume_info: Optional[str] = None\n\n\n@dataclass\nclass TwoEuro:\n    """A two euro coin to collect."""\n\n    feature: str = ""\n    description: str = ""\n    coinages: List[Coinage] = field(default_factory=list)\n```\n\n## Roadmap\n\n- [ ] Implement national side scraping (2€, 1€, 50 cent, 20 cent, 10 cent, 5 cent, 2 cent and 1 cent)\n- [ ] CLI implementation with click\n\n## Development\n\n### Creating a new release\n\n#### A. Create annotated release tag\n\n1. New tag\n```\ngit tag -a v<major>.<minor>.<patch>(a|b) -m release v<major>.<minor>.<patch>(a|b)\n```\n2. Push created tag\n\n```\ngit push --tags\n```\n#### B. Create GitHub release\n\n1. Run the following command `poetry version <version>`\n<br>*cointainer-scraper-ecb* uses the following schema: `^\\d+\\.\\d+\\.\\d+((b|a)\\d+)?$`\n\n2. Bump the version within the file: `cointainer_scraper_ecb/__init__.py`\n<br>Make sure it\'s the same version used when bumping with poetry\n\n3. Open `CHANGELOG.md` and write the new changelog:\n    - Use the following `#` header: `v<version> - (yyyy-mm-dd)`\n    <br>Used `##` headers:\n    - 💌 Added\n    - 🔨 Fixed\n    - ♻️ Changed\n\n4. Stage the modified files and push them with the following commit message:\n> chore: bump to version `v<version>`\n\n1. Create annotated release tag\n   1.  New tag\n    ```\n    git tag -s -m "release v<version>" v<version>\n    ```\n   2. Push created tag\n\n    ```\n    git push --tags\n    ```\n\n2. Run the following command `poetry build` to create a tarball and a wheel based on the new version\n\n3. Create a new github release and:\n    1. Copy and paste the changelog content **without** the `#` header into the *description of the release* textbox\n    2. Use the `#` header style to fill in the *Release title* (copy it from the `CHANGELOG.md`)\n    3. Copy the version with the `v`-prefix into the *Tag version*\n\n4. Attach the produced tarball and wheel (`dist/`) to the release\n\n5. Check *This is a pre-release* if it\'s either an alpha or beta release *(a|b)* - ***optional*** \n\n6.  **Publish release**\n\n### Testing\n\nUse the following command to execute the tests:\n\n```bash\npoetry run pytest\n```\n\nTo run the tests, the: `download-test-files.(ps1|sh)` script must be executed.\n\nThis is not the best method because the test data can change. However, I don\'t know if it is allowed to upload the data to the repository because of the copyright.\n\n## License\nThis cointainer-scraper-ecb module is distributed under Apache-2.0. For ODbL-1.0 exception, see [LICENSING.md](https://github.com/cointainer/cointainer-scraper-ecb/blob/main/LICENSING.md)',
    'author': 'B4rtware',
    'author_email': '34386047+B4rtware@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cointainer/cointainer-scraper-ecb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
