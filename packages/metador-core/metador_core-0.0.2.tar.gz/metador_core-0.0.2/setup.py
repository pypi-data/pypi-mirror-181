# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metador_core',
 'metador_core.container',
 'metador_core.harvester',
 'metador_core.ih5',
 'metador_core.packer',
 'metador_core.plugin',
 'metador_core.schema',
 'metador_core.schema.common',
 'metador_core.util',
 'metador_core.widget',
 'metador_core.widget.jupyter',
 'metador_core.widget.server']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.3,<3.0.0',
 'Pillow>=9.1.1,<10.0.0',
 'Pint>=0.18,<0.19',
 'frozendict>=2.3.4,<3.0.0',
 'h5py>=3.6.0,<4.0.0',
 'importlib-metadata>=4.11.4,<5.0.0',
 'isodate>=0.6.1,<0.7.0',
 'jsonschema>=4.4.0,<5.0.0',
 'overrides>=7.0.0,<8.0.0',
 'pandas>=1.4.1,<2.0.0',
 'panel>=0.14.0,<0.15.0',
 'phantom-types>=0.17.1,<0.18.0',
 'pydantic-yaml[ruamel]>=0.6.3,<0.7.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-magic>=0.4.25,<0.5.0',
 'simple-parsing>=0.0.20,<0.0.21',
 'toml>=0.10.2,<0.11.0',
 'typing-extensions>=4.1.1,<5.0.0',
 'typing-utils>=0.1.0,<0.2.0',
 'wrapt>=1.14.1,<2.0.0']

entry_points = \
{'metador_harvester': ['core.file.generic__0.1.0 = '
                       'metador_core.harvester.common:FileMetaHarvester',
                       'core.imagefile.dim__0.1.0 = '
                       'metador_core.harvester.common:ImageFileMetaHarvester'],
 'metador_packer': ['core.generic__0.1.0 = '
                    'metador_core.packer.example:GenericPacker'],
 'metador_plugingroup': ['harvester__0.1.0 = '
                         'metador_core.harvester:PGHarvester',
                         'packer__0.1.0 = metador_core.packer:PGPacker',
                         'schema__0.1.0 = metador_core.schema.pg:PGSchema',
                         'widget__0.1.0 = metador_core.widget:PGWidget'],
 'metador_schema': ['core.bib__0.1.0 = metador_core.schema.common:BibMeta',
                    'core.dashboard__0.1.0 = '
                    'metador_core.widget.dashboard:DashboardMeta',
                    'core.dir__0.1.0 = '
                    'metador_core.schema.common.rocrate:DirMeta',
                    'core.file__0.1.0 = '
                    'metador_core.schema.common.rocrate:FileMeta',
                    'core.imagefile__0.1.0 = '
                    'metador_core.schema.common:ImageFileMeta',
                    'core.packerinfo__0.1.0 = metador_core.packer:PackerInfo',
                    'core.table__0.1.0 = metador_core.schema.common:TableMeta'],
 'metador_widget': ['core.file.audio__0.1.0 = '
                    'metador_core.widget.common:AudioWidget',
                    'core.file.image__0.1.0 = '
                    'metador_core.widget.common:ImageWidget',
                    'core.file.json__0.1.0 = '
                    'metador_core.widget.common:JSONWidget',
                    'core.file.pdf__0.1.0 = '
                    'metador_core.widget.common:PDFWidget',
                    'core.file.text.code__0.1.0 = '
                    'metador_core.widget.common:CodeWidget',
                    'core.file.text.html__0.1.0 = '
                    'metador_core.widget.common:HTMLWidget',
                    'core.file.text.md__0.1.0 = '
                    'metador_core.widget.common:MarkdownWidget',
                    'core.file.text__0.1.0 = '
                    'metador_core.widget.common:TextWidget',
                    'core.file.video__0.1.0 = '
                    'metador_core.widget.common:VideoWidget']}

setup_kwargs = {
    'name': 'metador-core',
    'version': '0.0.2',
    'description': 'Core of Metador, the metadata-first research data management framework.',
    'long_description': '# metador-core\n\n![Project status](https://img.shields.io/badge/project%20status-alpha-%23ff8000)\n[\n![Test](https://img.shields.io/github/workflow/status/Materials-Data-Science-and-Informatics/metador-core/test?label=test)\n](https://github.com/Materials-Data-Science-and-Informatics/metador-core/actions?query=workflow:test)\n[\n![Coverage](https://img.shields.io/codecov/c/gh/Materials-Data-Science-and-Informatics/metador-core?token=4JU2SZFZDZ)\n](https://app.codecov.io/gh/Materials-Data-Science-and-Informatics/metador-core)\n[\n![Docs](https://img.shields.io/badge/read-docs-success)\n](https://materials-data-science-and-informatics.github.io/metador-core/)\n\nCore library of the Metador platform. It provides:\n\n* an interface for managing structured and validated metadata (`MetadorContainer`)\n* an API to manage immutable (but still "patchable") HDF5 files (`IH5Record`)\n* an extensible entry-points based plugin system defining plugin groups and plugins\n* core plugin group interfaces (schemas, packers, widgets, ...)\n* general semantically aligned schemas that should be used and extended\n* visualization widgets for common data types based on Bokeh and Panel\n* generic dashboard presenting (meta)data for which suitable widgets are installed\n\n## Getting Started\n\nThis library is not a batteries-included solution, it is intended for people interested in\nusing and extending the Metador ecosystem and who are willing to write their own plugins\nto adapt Metador to their use-case and provide services based on it.\n\nPlease check out the tutorials that explain general concepts,\ninterfaces and specific plugin development topics are provided [here](./tutorial).\n\nFor a first taste, you can install this package just as any other package into your\ncurrent Python environment using:\n\n<!--\nold install link based on https:\nmetador-core@git+https://github.com/Materials-Data-Science-and-Informatics/metador-core.git\n-->\n\n```\n$ pip install git+ssh://git@github.com:Materials-Data-Science-and-Informatics/metador-core.git\n```\n\nor if you are adding it as a dependency into your poetry project:\n\n```\n$ poetry add git+ssh://git@github.com:Materials-Data-Science-and-Informatics/metador-core.git\n```\n\nAs usual, it is highly recommended that you use a\n[virtual environment](https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe)\nto ensure isolation of dependencies between unrelated projects.\n\nIf you want to write or extend plugins, such as metadata schemas or widgets,\nthe provided tutorials will get you started.\n\nIf you want to contribute to the actual core, see further below.\n\n## Compatibility and Known Issues\n\nThis package supports Python `>=3.8`.\n\nThere was a mysterious bug when using inside Jupyter `6.4.6`,\nbut there are no known problems when upgrading to Jupyter `6.4.10`.\n\nIf you encounter any problems, ensure that your bug is reproducible in a simple and\nminimal standalone Python script that is runnable in a venv with this package installed\nand can demonstrate your issue.\n\n## Development\n\nThis project uses [Poetry](https://python-poetry.org/) for dependency\nmanagement, so you will need to have poetry\n[installed](https://python-poetry.org/docs/master/#installing-with-the-official-installer)\nin order to contribute.\n\nThen you can run the following lines to setup the project and install the package:\n```\n$ git clone git@github.com:Materials-Data-Science-and-Informatics/metador-core.git\n$ cd metador-core\n$ poetry install\n```\n\nRun `pre-commit install` (see [https://pre-commit.com](https://pre-commit.com))\nafter cloning. This enables pre-commit to enforce the required linting hooks.\n\nRun `pytest` (see [https://docs.pytest.org](https://docs.pytest.org)) before\nmerging your changes to make sure you did not break anything. To check\ncoverage, use `pytest --cov`.\n\nTo generate local documentation (as the one linked above), run\n`pdoc -o docs metador_core` (see [https://pdoc.dev](https://pdoc.dev)).\n\n## Acknowledgements\n\n<div>\n<img style="vertical-align: middle;" alt="HMC Logo" src="https://github.com/Materials-Data-Science-and-Informatics/Logos/raw/main/HMC/HMC_Logo_M.png" width=50% height=50% />\n&nbsp;&nbsp;\n<img style="vertical-align: middle;" alt="FZJ Logo" src="https://github.com/Materials-Data-Science-and-Informatics/Logos/raw/main/FZJ/FZJ.png" width=30% height=30% />\n</div>\n<br />\n\nThis project was developed at the Institute for Materials Data Science and Informatics\n(IAS-9) of the Jülich Research Center and funded by the Helmholtz Metadata Collaboration\n(HMC), an incubator-platform of the Helmholtz Association within the framework of the\nInformation and Data Science strategic initiative.\n',
    'author': 'Anton Pirogov',
    'author_email': 'a.pirogov@fz-juelich.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Materials-Data-Science-and-Informatics/metador-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
