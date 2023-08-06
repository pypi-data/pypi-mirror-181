# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lapidary', 'lapidary.render', 'lapidary.render.model']

package_data = \
{'': ['*'],
 'lapidary.render': ['templates/*',
                     'templates/auth/*',
                     'templates/client/*',
                     'templates/init/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'black>=22.8.0,<23.0.0',
 'inflection>=0.5.1,<0.6.0',
 'jsonpatch>=1.32,<2.0',
 'lapidary==0.7.3',
 'pydantic>=1.10.2,<2.0.0',
 'python-mimeparse>=1.6.0,<2.0.0',
 'tomlkit>=0.11.4,<0.12.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['lapidary = lapidary.render:app']}

setup_kwargs = {
    'name': 'lapidary-render',
    'version': '0.7.3',
    'description': 'Python async OpenAPI client library generator',
    'long_description': "# Code generator\n## Installation\n\nlapidary-render requires python 3.9 or higher to run.\n\nI recommend installing via `pipx`\n\n`pipx install lapidary-render`\n\nYou can set python version for lapidary with `pipx install --python [path-to-python] lapidary-render`. See `pipx install --help` for details.\n\n## Usage\n\n`lapidary` command offers inline help and shell command completion. See `lapidary --help` for details.\n\n### lapidary init\n\n`lapidary init [--[no-]format] [--[no-]render] SCHEMA_PATH PROJECT_ROOT PACKAGE_NAME`\n\nLapidary will create \n- PROJECT_ROOT and all necessary directories,\n- \\_\\_init\\_\\_.py files,\n- pyproject.toml with [poetry](https://python-poetry.org/) configured,\n- py.typed\n- client.pyi with function stubs for all operations and a client.py with an empty client class.\n- [Pydantic](https://docs.pydantic.dev/) model classes for each schema.\n\nAll python files are generated in PROJECT_ROOT/gen directory.\n\nIf a directory PROJECT_ROOT/src/patches exists, Lapidary will read all yaml files and apply them as JSONPatch against the original openapi file.\n\nIf the original openapi file is not compatible with Lapidary, running `lapidary init --no-render ...` will generate only the project structure without any\nmodels or stubs. Once you've prepared the patch, run `lapidary update`.\n\n### lapidary update\n\n`lapidary update [--[no-]format] [--[no-]cache] [PROJECT_ROOT]`\n\nDefault PROJECT_ROOT is the current directory.\n\nThe command\n- deletes PROJECT_ROOT/gen directory,\n- re-applies patches to openapi file\n- and generates python files\n\n### lapidary version\n\n`lapidary version`\n\nPrints the programs version and exits.\n\n## Configuration\n\nLapidary can be configured with a pyproject.yaml file, under [tool.lapidary] path.\n\nOnly `package` value is required, and it's set by `lapidary init`.\n\n- package [str] - root package name \n- format [bool] - whether to format the generated code with black [default = True].\n- cache [bool] - whether to cache openapi and patches as pickle files. Only files larger than 50kB are cached [default = True].\n- src_root [str] - sources root, in PROJECT_ROOT [default = 'src'].\n- gen_root [str] = generated sources root, in PROJECT_ROOT [default = 'gen'].\n- patches [str] = patches directory, under sources root [default = 'patches'].\n",
    'author': 'Raphael Krupinski',
    'author_email': 'rafalkrupinski@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/python-lapidary/lapidary',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
