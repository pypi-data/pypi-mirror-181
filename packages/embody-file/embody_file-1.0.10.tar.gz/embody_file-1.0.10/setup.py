# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['embodyfile']

package_data = \
{'': ['*']}

install_requires = \
['embody-codec>=1.0.15', 'matplotlib>=3.6.2', 'pandas>=1.5.1', 'tables>=3.7.0']

entry_points = \
{'console_scripts': ['embody-file = embodyfile.cli:main']}

setup_kwargs = {
    'name': 'embody-file',
    'version': '1.0.10',
    'description': 'Embody file converter',
    'long_description': "# Embody File\n\n[![PyPI](https://img.shields.io/pypi/v/embody-file.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/embody-file.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/embody-file)][python version]\n[![License](https://img.shields.io/pypi/l/embody-file)][license]\n\n[![Tests](https://github.com/aidee-health/embody-file/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/embody-file/\n[status]: https://pypi.org/project/embody-file/\n[python version]: https://pypi.org/project/embody-file\n[tests]: https://github.com/aidee-health/embody-file/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nThis is a Python based implementation for parsing binary files from the Aidee EmBody device.\n\n## Features\n\n- Converts binary embody files to HDF, CSV, etc\n- Integrates with [the EmBody Protocol Codec](https://github.com/aidee-health/embody-protocol-codec) project\n- CLI (command line interface)\n- Can be used as package in other projects\n- Type safe code using [mypy](https://mypy.readthedocs.io/) for type checking\n\n## Requirements\n\n- Python 3.8-3.10\n\n## Installation\n\nYou can install _Embody File_ via [pip]:\n\n```console\n$ pip install embody-file\n```\n\n## Usage\n\nTo use the command line, first install this library either globally or using venv:\n\n```console\n$ pip install embody-file\n```\n\nWhen this library has been installed, a new command is available, `embody-file` which can be used according to the examples below:\n\n### Get help\n\nTo get an updated overview of all command line options:\n\n```bash\nembody-file --help\n```\n\n### Print version number\n\n```bash\nembody-file --version\n```\n\n### Convert binary embody file to HDF\n\nTo convert to a [HDF 5 (hierarcical data format)](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) format, run the following:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --output-format HDF\n```\n\nThe file will be named the same as the input file, with the `.hdf` extension at the end of the file name.\n\n### Convert binary embody file to CSV\n\nTo convert to CSV format, run the following:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --output-format CSV\n```\n\nThe file will be named the same as the input file, with the `.csv` extension at the end of the file name.\n\n### Print statistics for binary embody file\n\nTo print stats without conversion:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --print-stats\n```\n\n### Fail on parse errors\n\nThe parser is lenient by default, accepting errors in the input file. If you want to the parsing to fail on any errors, use the `--strict` flag:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --strict\n```\n\n### Plot binary file in graph\n\nTo show an ECG/PPG plot graph:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --plot\n```\n\n## Troubleshooting\n\n### I get an error in the middle of the file - how do I start finding the root cause?\n\nTo get the best overview, start by running the parser in strict mode and with debug logging, so it stops at the first error:\n\n```bash\nembody-file troublesomefile.log --strict --log-level DEBUG\n```\n\nThis provides positional information per message so it's easier to continue searching for errors.\n\nIf this doesn't give us enough information, look at the protocol documentation and start looking and the problematic areas in the input file.\n\nThere are several command line tools you can use. On MAC and Linux, one good example is to use the `hexdump` tool:\n\n```bash\nhexdump -C -n 70 -s 0 troublesomefile.log\n```\n\nHere, `-n 70` is the amount of bytes to print in hex format, and `-s 0` tells hexdump to start at position 0 in the file. Adjust these parameters according to your needs.\n\nMake a note from the parser's error output of what position the first error started from, and based on that:\n\n- Look at the preceding bytes to see whether there were any errors in the previous protocol message\n- Look at the bytes from the reported (error) position to see if there are just a few bytes before a new, plausible protocol message starts\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[file an issue]: https://github.com/aidee-health/embody-file/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/aidee-health/embody-file/blob/main/LICENSE\n[contributor guide]: https://github.com/aidee-health/embody-file/blob/main/CONTRIBUTING.md\n[command-line reference]: https://embody-file.readthedocs.io/en/latest/usage.html\n",
    'author': 'Aidee Health',
    'author_email': 'hello@aidee.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aidee-health/embody-file',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
