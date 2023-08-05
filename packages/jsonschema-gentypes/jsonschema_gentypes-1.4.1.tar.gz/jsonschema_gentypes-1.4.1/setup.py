# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_gentypes']

package_data = \
{'': ['*']}

install_requires = \
['certifi', 'jsonschema', 'ruamel.yaml']

extras_require = \
{'extra': ['pinyin', 'romkan', 'romanize'],
 'generate': ['requests', 'PyYAML'],
 'tools': ['pyupgrade', 'black', 'isort']}

entry_points = \
{'console_scripts': ['jsonschema-gentypes = jsonschema_gentypes.cli:main']}

setup_kwargs = {
    'name': 'jsonschema-gentypes',
    'version': '1.4.1',
    'description': 'Tool to generate Python types based on TypedDict from a JSON Schema',
    'long_description': '# JSON Schema generate Python types\n\nTools to generate Python types based on TypedDict from a JSON schema\n\n## Quick start\n\ninstall:\n\n```bash\npython3 -m pip install --user jsonschema-gentypes\n```\n\nConvert a JSON schema to a Python file contains the types:\n\n```bash\njsonschema-gentypes --json-schema=<JSON schema> --python=<destination Python file>\n```\n\n## Docker\n\nYou can also run it with Docker:\n\n```bash\ndocker run --rm --user=$(id --user) --volume=$(pwd):/src camptocamp/jsonschema-gentypes\n```\n\n## Config file\n\nYou can also write a config file named `jsonschema-gentypes.yaml` with:\n\n```yaml\nheaders: >\n  # Automatically generated file from a JSON schema\n# Used to correctly format the generated file\ncallbacks:\n  - - black\n  - - isort\ngenerate:\n  - # JSON schema file path\n    source: jsonschema_gentypes/schema.json\n    # Python file path\n    destination: jsonschema_gentypes/configuration.py\n    # The name of the root element\n    root_name: Config\n    # Argument passed to the API\n    api_arguments:\n      additional_properties: Only explicit\n    # Rename an element\n    name_mapping: {}\n```\n\nAnd just run:\n\n```bash\njsonschema-gentypes\n```\n\n# Default\n\nThe default values are exported in the Python file, then you can do something like that:\n\n```python\nvalue_with_default = my_object.get(\'field_name\', my_schema.FIELD_DEFAULT)\n```\n\n# Validation\n\nThis package also provide some validations features for YAML file based on `jsonschema`.\n\nAdditional features:\n\n- Obtain the line and columns number in the errors, if the file is loaded with `ruamel.yaml`.\n- Export the default provided in the JSON schema.\n\n```python\n    import ruamel.yaml\n    import pkgutil\n    import jsonschema_gentypes.validate\n\n    schema_data = pkgutil.get_data("jsonschema_gentypes", "schema.json")\n    with open(filename) as data_file:\n        yaml = ruamel.yaml.YAML()  # type: ignore\n        data = yaml.load(data_file)\n    errors, data = jsonschema_gentypes.validate.validate(filename, data, schema)\n    if errors:\n        print("\\n".join(errors))\n        sys.exit(1)\n```\n\nThe filling of the default value is deprecated because it can produce quite peculiar things, see also\n[the jsonschema documentation](https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance).\n\n## Limitations\n\nRequires Python 3.8\n\nSee the [issues with label "limitation"](https://github.com/camptocamp/jsonschema-gentypes/issues?q=is%3Aissue+is%3Aopen+label%3Alimitation).\n\n## Contribute\n\nThe code should be formatted with `isort` and `black`.\n\nThe code should be typed.\n\nThe `prospector` tests should pass.\n\nThe code should be tested with `pytests`.\n',
    'author': 'Camptocamp',
    'author_email': 'info@camptocamp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/camptocamp/jsonschema-gentypes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
