# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ldimbenchmark',
 'ldimbenchmark.datasets',
 'ldimbenchmark.datasets.loaders',
 'ldimbenchmark.generator',
 'ldimbenchmark.methods']

package_data = \
{'': ['*']}

install_requires = \
['big-o>=0.10.2,<0.11.0',
 'click>=8.1.3,<9.0.0',
 'docker>=6.0.1,<7.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.64.1,<5.0.0',
 'wntr>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['ldimbenchmark = ldimbenchmark.cli:cli']}

setup_kwargs = {
    'name': 'ldimbenchmark',
    'version': '0.1.16',
    'description': '',
    'long_description': '# LDIMBenchmark\n\nLeakage Detection and Isolation Methods Benchmark\n\n## Usage\n\n### Installation\n\n```bash\npip install ldimbenchmark\n```\n\n### Python\n\n```python\nfrom ldimbenchmark.datasets import DatasetLibrary, DATASETS\nfrom ldimbenchmark import (\n    LDIMBenchmark,\n    BenchmarkData,\n    BenchmarkLeakageResult,\n)\nfrom ldimbenchmark.classes import LDIMMethodBase\nfrom typing import List\n\nclass YourCustomLDIMMethod(LDIMMethodBase):\n    def __init__(self):\n        super().__init__(\n            name="YourCustomLDIMMethod",\n            version="0.1.0"\n        )\n\n    def train(self, data: BenchmarkData):\n        pass\n\n    def detect(self, data: BenchmarkData) -> List[BenchmarkLeakageResult]:\n        return [\n            {\n                "leak_start": "2020-01-01",\n                "leak_end": "2020-01-02",\n                "leak_area": 0.2,\n                "pipe_id": "test",\n            }\n        ]\n\n    def detect_datapoint(self, evaluation_data) -> BenchmarkLeakageResult:\n        return {}\n\n\ndatasets = DatasetLibrary("datasets").download(DATASETS.BATTLEDIM)\n\nlocal_methods = [YourCustomLDIMMethod()]\n\nhyperparameters = {}\n\nbenchmark = LDIMBenchmark(\n    hyperparameters, datasets, results_dir="./benchmark-results"\n)\nbenchmark.add_local_methods(local_methods)\n\nbenchmark.run_benchmark()\n\nbenchmark.evaluate()\n```\n\n### CLI\n\n```bash\n# TODO (not yet working)\nldimbenchmark --help\n```\n\n## Roadmap\n\n- v1: Just Leakage Detection\n- v2: Provides Benchmark of Isolation Methods\n\nhttps://mathspp.com/blog/how-to-create-a-python-package-in-2022\n\n## Development\n\nhttps://python-poetry.org/docs/basic-usage/\n\n```bash\n# python 3.10\n# Use Environment\npoetry config virtualenvs.in-project true\npoetry shell\npoetry install --without ci # --with ci\n\n\n# Test\npoetry build\ncp -r dist tests/dist\ncd tests\ndocker build . -t testmethod\npytest -s -o log_cli=true\npytest tests/test_derivation.py -k \'test_mything\'\n# Pytest watch\nptw\nptw -- --testmon\n\n\n# Test-Publish\npoetry config repositories.testpypi https://test.pypi.org/legacy/\npoetry config http-basic.testpypi __token__ pypi-your-api-token-here\npoetry build\npoetry publish -r testpypi\n\n# Real Publish\npoetry config pypi-token.pypi pypi-your-token-here\n```\n\n### Documentation\n\nhttps://squidfunk.github.io/mkdocs-material/\nhttps://click.palletsprojects.com/en/8.1.x/\n\n```\nmkdocs serve\n```\n',
    'author': 'DanielHabenicht',
    'author_email': 'daniel-habenicht@outlook.de',
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
