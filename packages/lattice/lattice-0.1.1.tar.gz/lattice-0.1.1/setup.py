# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lattice', 'lattice.docs']

package_data = \
{'': ['*'],
 'lattice.docs': ['hugo_layouts/*',
                  'hugo_layouts/_default/*',
                  'hugo_layouts/landing/*',
                  'hugo_layouts/partials/*',
                  'hugo_layouts/specifications/*']}

install_requires = \
['Jinja2',
 'cbor2',
 'jsonschema',
 'pygit2>=1.10.0,<2.0.0',
 'pyyaml',
 'stringcase==1.2.0']

setup_kwargs = {
    'name': 'lattice',
    'version': '0.1.1',
    'description': 'A framework for developing data models, including schema development and documentation.',
    'long_description': '[![Release](https://img.shields.io/pypi/v/lattice.svg)](https://pypi.python.org/pypi/lattice)\n\n[![Build and Test](https://github.com/bigladder/lattice/actions/workflows/build-and-test.yaml/badge.svg)](https://github.com/bigladder/lattice/actions/workflows/build-and-test.yaml)\n\n[![Web Documentation](https://github.com/bigladder/lattice/actions/workflows/release.yaml/badge.svg)](https://github.com/bigladder/lattice/actions/workflows/release.yaml)\n\nLattice\n===========\n\nA Python package that provides support for a schema-based building data model framework, currently under development as ASHRAE Standard 232P, where schema are described in compliant YAML source files. Lattice performs:\n\n- Data model validation: Ensures the YAML schema source files are well-formed.\n- Schema generation: Translates the YAML schema source files into equivalent JSON Schema.\n- Data file validation: Validates data files against the generated JSON Schema and additional validation requirements not supported by JSON Schema (e.g., reference checking).\n- Data model documentation: Generates web documentation of the data model from the YAML schema source files and templated markdown files (requires [Go](https://go.dev/), [Hugo](https://gohugo.io/installation/), and [Node.js](https://nodejs.org/en/download/)). This web documentation can be automatically deployed to GitHub pages.\n\nFuture additions under development include:\n\n- Generation of PDF documentation of the data model.\n- Generation of C/C++ source code for processing compliant data files.\n\n\nInstalling\n----------\n\nTo install Lattice, simply:\n\n`pip install lattice`\n\nTo generate data model documentation, you\'ll also need to install:\n\n- [Go](https://go.dev/)\n- [Hugo](https://gohugo.io/installation/)\n- [Node.js](https://nodejs.org/en/download/)\n\nExample Usage\n-------------\n\n_lattice_ is Python package defining the `Lattice` class. Lattice relies on a predetermined structure of subdirectories:\n\n- **schema** (optional): Contains YAML source schema files describing the data model. Alternatively, if YAML source schema files are not provided in a "schema" directory, they must be in the root directory.\n- **docs** (optional): Contains markdown templates that are used to render model documentation. An optional subdirectory of "docs" called "web" contains additional content required for generating the web documentation including configuration settings, graphics, and supplementary content.\n- **examples** (optional): Example data files compliant with the data model.\n\nThe `Lattice` class is instantiated with the following parameters:\n\n- `root_directory`: This is the directory containing the source subdirectories.The default is the current working directory.\n\n- `build_directory`: This is the path to the directory where the content related to lattice is stored. The content itself will be located in a subdirectory determined by `build_output_directory_name` (below). It includes intermediate meta-schema(s), JSON Schema(s), generated markdown files, and the generated web documentation. The default is `root_directory`.\n\n- `build_output_directory_name`: The name of the lattice output content directory. The default is `".lattice/"`.\n\n- `build_validation`: A boolean indicator to automatically generate meta-schema, validate the data model, generate the schemas and validate the example data files upon instantiation. If false, these tasks must be executed after instantiation using the `generate_meta_schemas`, `validate_schemas`, `generate_json_schemas`, and `validate_example_files` methods. The default is `True`.\n\nThe repository\'s *examples* directory contains sample data models exemplifying different model options, such as Data Group Templates or scoped references.\n\nMore complete examples of projects using the ASHRAE Standard 232P framework include:\n\n- [IBPSA-USA Climate Information](https://github.com/IBPSA-USA/climate-information) (uses lattice)\n- [ASHRAE Standard 205](https://github.com/open205/schema-205) (transitioning to lattice)\n- [ASHRAE Standard 229](https://github.com/open229/ruleset-model-description-schema) (does not use lattice...yet)\n\n',
    'author': 'Big Ladder Software',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bigladder/lattice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
