# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['retimer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'retimer',
    'version': '0.1.0.6',
    'description': '',
    'long_description': '# retimer\n\n > A simple package to make retry loops easier\n\n[![PyPI version][pypi-image]][pypi-url]\n[![Build status][build-image]][build-url]\n[![GitHub stars][stars-image]][stars-url]\n[![Support Python versions][versions-image]][versions-url]\n\n\n\n## Getting started\n\nYou can [get `retimer` from PyPI](https://pypi.org/project/retimer),\nwhich means it\'s easily installable with `pip`:\n\n```bash\npython -m pip install extendedjson\n```\n\n\n\n\n## Example usage\nThink of a scenario where you need to keep trying to do something for a range of time, usually you can write this:\n\n```python\nfrom time import perfcounter\n\ntimeout = 10\nbegin = perfcounter()\nwhile percounter() - begin < timeout:\n     # do something for 10 seconds\n     \n     if retry_doing_something:\n         time.sleep(.5)\n         continue\n         \n     if something_bad:\n         break\n         \n     # all good\n     break\n     \nif perfcounter - begin >= timeout:\n    print(f"Could not do something after {timeout} seconds")\nelse:\n    print("Success!")\n```\n\n\nRewriting using this package becomes:\n```python\nfrom retimer import Timer\nimport time\n\ntimer = Timer(10)\nwhile timer.not_expired:\n    # do something for 10 seconds\n    \n    if retry_doing_something:\n        time.sleep(.5)\n        continue\n        \n    if something_bad:\n        timer.explode()\n    \n    # all good\n    break\n    \nif timer.expired:\n    print(f"Could not do something after {timer.duration} seconds")\nelse:\n    print("Success!")\n    \n```\n\nAlthough both codes accomplish the same result, I personally find the second one more readable and shines when I need two or more chained loops\n\n## Changelog\n\nRefer to the [CHANGELOG.md](https://github.com/henriquelino/retimer/blob/main/CHANGELOG.md) file.\n\n\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/retimer\n[pypi-url]: https://pypi.org/project/retimer/\n\n[build-image]: https://github.com/henriquelino/retimer/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/henriquelino/retimer/actions/workflows/build.yaml\n\n[stars-image]: https://img.shields.io/github/stars/henriquelino/retimer\n[stars-url]: https://github.com/henriquelino/retimer\n\n[stars-image]: https://img.shields.io/github/stars/mathspp/extendedjson\n[stars-url]: https://github.com/mathspp/extendedjson\n\n[versions-image]: https://img.shields.io/pypi/pyversions/retimer\n[versions-url]: https://pypi.org/project/retimer/\n\n',
    'author': 'henrique lino',
    'author_email': 'henrique.lino97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
