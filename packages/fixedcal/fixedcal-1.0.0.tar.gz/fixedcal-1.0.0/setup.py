# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixedcal', 'fixedcal.core', 'fixedcal.services']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fixedcal',
    'version': '1.0.0',
    'description': 'Fixed calendar package',
    'long_description': "# FixedCal\n\n[![CI](https://github.com/PyryL/fixedcal/actions/workflows/main.yml/badge.svg)](https://github.com/PyryL/fixedcal/actions)\n[![codecov](https://codecov.io/gh/PyryL/fixedcal/branch/main/graph/badge.svg?token=ZMYYLBUPNA)](https://codecov.io/gh/PyryL/fixedcal)\n[![GitHub](https://img.shields.io/github/license/PyryL/fixedcal)](LICENSE)\n\nPython package for international fixed calendar dates.\n\n## What is that?\n\nInternational fixed calendar is an alternative calendar system.\nIt divides year into 13 even months by adding a month called Sol between June and July.\nEach month starts with Sunday and has exactly 28 days or 4 weeks.\nAn additional _year day_ is added to the end of the year and it does not belong to any of the months and has no weekday.\nYou can read more about IFC on [Wikipedia](https://en.wikipedia.org/wiki/International_Fixed_Calendar).\n\n## Installation\n\nThis package is available via PyPI:\n\n```\npip install fixedcal\n```\n\nYou can also download the package directly from [releases](https://github.com/PyryL/fixedcal/releases).\n\n## Usage\n\n### Date initialization\n\n```python3\nfrom fixedcal import FixedDate\n\n# Date of today\nfixed_date = FixedDate.today()\n\n# From native datetime\nimport datetime\nfebruary_seventh = datetime.date(2022, 2, 7)\nfixed_date = FixedDate(february_seventh)\n\n# From day's ordinal in year\nfixed_date = FixedDate(day_of_year=107, year=2022)\n```\n\n### Date's properties\n\n```python3\nfrom fixedcal import FixedDate\nimport datetime\nfixed_date = FixedDate(datetime.date(2022, 8, 12))\n\nfixed_date.date           # datetime.date(2022, 8, 12)\nfixed_date.day_of_year    # 224\nfixed_date.day_of_month   # 28\nfixed_date.month          # 8\nfixed_date.year           # 2022\nfixed_date.is_year_day    # False\nfixed_date.is_leap_day    # False\nfixed_date.is_leap_year   # False\nfixed_date.week_of_month  # 4\nfixed_date.weekday        # 7\nfixed_date.week_of_year   # 32\nfixed_date.year_quarter   # 3\n```\n\n### Date's operations\n\n```python3\nfrom fixedcal import FixedDate\nfrom datetime import date, timedelta\n\nfixed_date = FixedDate(date(2022, 12, 6))\njan_first = FixedDate(date(2023, 1, 1))\n\nstr(fixed_date)                       # 2022-13-04\n\nnew_fixed = fixed_date + timedelta(3) # FixedDate 3 days ahead\nnew_fixed = fixed_date - timedelta(2) # FixedDate 2 days before\nnew_fixed = jan_first - fixed_date    # timedelta between dates\n\nfixed_date == fixed_date              # True\nfixed_date != jan_first\t              # True\njan_first < fixed_date                # False\n```\n\n### Year day\n\nYear day is the day after the last of December and before the first of January.\nFor that date, `FixedDate` gives the following property values.\n\n* `day_of_year` = 365 (366 on leap years)\n* `day_of_month` = 29\n* `month` = 13\n* `year` is obviously the ending year\n* `is_year_day` = True\n* `week_of_month` = 4\n* `weekday` = None\n* `week_of_year` = 52\n* `year_quarter` = 4\n\n### Leap day\n\nLeap day occurres on the same years as in Gregorian calendar. However, the placement of that day is different: after the last day of June and before the first day of Sol (17th June in Gregorian). The following properties are given by `FixedDate` for leap day:\n\n* `day_of_year` = 169\n* `day_of_month` = 29\n* `month` = 6\n* `is_leap_day` = True\n* `is_leap_year` = True\n* `week_of_month` = 4\n* `weekday` = None\n* `week_of_year` = 24\n* `year_quarter` = 2\n\n## Contributing\n\nYes, you can contribute in the development of this package. If you find a bug or have a feature request, please file an [issue](https://github.com/PyryL/fixedcal/issues/new). You can also modify the code yourself and create a pull request.\n\nYou need [Poetry](https://python-poetry.org/) to manage the development environment. After downloading the source code of this package, run `poetry install` to install development dependencies and to set up a compatible Python environment.\n\nPlease check the following topics before creating a pull request:\n\n* Your changes should not create new Pylint errors.\n* There should be proper unit tests included in the pull request. This consists of high branch coverage (>90%) and quality of the tests. Working with dates has a lot of corner cases and tests are the best way to avoid bugs.\n* The structure of the project should remain healthy: split the code between modules and packages.\n",
    'author': 'Pyry Lahtinen',
    'author_email': 'pyry@pyry.info',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PyryL/fixedcal',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
