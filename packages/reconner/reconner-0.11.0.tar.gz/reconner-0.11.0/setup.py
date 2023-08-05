# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recon', 'recon.cli', 'recon.operations', 'recon.prodigy']

package_data = \
{'': ['*'], 'recon.prodigy': ['templates/*']}

install_requires = \
['click-completion',
 'colorama',
 'numpy>=1.20.0',
 'pydantic>=1.9,<2.0',
 'scipy>=1.7.0,<1.9',
 'spacy>=3.2.0,<3.5.0',
 'xxhash>=3.0.0,<4.0']

entry_points = \
{'console_scripts': ['recon = recon.cli:app'],
 'prodigy_recipes': ['recon.ner_correct = '
                     'recon:prodigy_recipes.recon_ner_correct_v1',
                     'recon.ner_merge = '
                     'recon:prodigy_recipes.recon_ner_merge_v1']}

setup_kwargs = {
    'name': 'reconner',
    'version': '0.11.0',
    'description': 'Recon NER, Debug and correct annotated Named Entity Recognition (NER) data for inconsitencies and get insights on improving the quality of your data.',
    'long_description': '<p align="center">\n  <a href="https://kabirkhan.github.io/recon"><img src="https://raw.githubusercontent.com/kabirkhan/recon/main/docs/img/recon-ner.svg" alt="Recon"></a>\n</p>\n<p align="center">\n    <em>Recon NER, Debug and correct annotated Named Entity Recognition (NER) data for inconsitencies and get insights on improving the quality of your data.</em>\n</p>\n<p align="center">\n<a href="https://pypi.org/project/reconner" target="_blank">\n    <img src="https://img.shields.io/pypi/v/reconner?style=for-the-badge" alt="PyPi Package version">\n</a>\n<a href="https://github.com/kabirkhan/recon/actions/workflows/ci.yml" target="_blank">\n    <img alt="GitHub Actions Build badge" src="https://img.shields.io/github/workflow/status/kabirkhan/recon/CI?style=for-the-badge">\n</a>\n<a href="https://codecov.io/gh/kabirkhan/recon" rel="nofollow">\n  <img alt="Codecov badge" src="https://img.shields.io/codecov/c/gh/kabirkhan/recon?style=for-the-badge" style="max-width:100%;">\n</a>\n\n<a href="https://pypi.org/project/reconner" target="_blank">\n    <img src="https://img.shields.io/pypi/l/reconner?style=for-the-badge" alt="PyPi Package license">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="https://kabirkhan.github.io/recon" target="_blank">https://kabirkhan.github.io/recon</a>\n\n**Source Code**: <a href="https://github.com/kabirkhan/recon" target="_blank">https://github.com/kabirkhan/recon</a>\n\n---\n\nRecon is a library to help you fix your annotated NER data and identify examples that are hardest for your model to predict so you can strategically prioritize the examples you annotate.\n\nThe key features are:\n\n* **Data Validation and Cleanup**: Easily Validate the format of your NER data. Filter overlapping Entity Annotations, fix missing properties.\n* **Statistics**: Get statistics on your data. From how many annotations you have for each label, to more complicated metrics like quality scores for the balance of your dataset.\n* **Model Insights**: Analyze how well your model does on your Dataset. Identify the top errors your model is making so you can prioritize data collection and correction strategically.\n* **Dataset Management**: Recon provides `Dataset` and `Corpus` containers to manage the train/dev/test split of your data and apply the same functions across all splits in your data + a concatenation of all examples. Operate inplace to consistently transform your data with reliable tracking and the ability to version and rollback changes.\n* **Serializable Dataset**: Serialize and Deserialize your data to and from JSON to the Recon type system.\n* **Type Hints**: Comprehensive Typing system based on Python 3.7+ Type Hints\n\n## Requirements\n\nPython 3.7 +\n\n* <a href="https://spacy.io" class="external-link" target="_blank">spaCy</a>\n* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic (Type system and JSON Serialization)</a>\n* <a href="https://typer.tiangolo.com" class="external-link" target="_blank">Typer (CLI)</a>.\n\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install reconner\n---> 100%\nSuccessfully installed reconner\n```\n\n</div>\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Kabir Khan',
    'author_email': 'kabirkhan1137@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kabirkhan.github.io/recon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
