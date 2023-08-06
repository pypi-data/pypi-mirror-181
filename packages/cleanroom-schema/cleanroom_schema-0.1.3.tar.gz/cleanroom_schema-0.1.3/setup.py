# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cleanroom_schema', 'cleanroom_schema.datamodel']

package_data = \
{'': ['*'], 'cleanroom_schema': ['schema/*']}

install_requires = \
['cruft>=2.11.1,<3.0.0',
 'deepdiff[cli]>=6.2.2,<7.0.0',
 'linkml-runtime>=1.1.24,<2.0.0',
 'schema-automator>=0.2.10,<0.3.0']

entry_points = \
{'console_scripts': ['test_publishability = '
                     'cleanroom_schema.test_publishability:print_nt']}

setup_kwargs = {
    'name': 'cleanroom-schema',
    'version': '0.1.3',
    'description': 'Cleanroom reboot of NMDC schema',
    'long_description': '# cleanroom-schema\n\nCleanroom reboot of NMDC schema\n\n## Website\n\n* [https://microbiomedata.github.io/cleanroom-schema](https://microbiomedata.github.io/cleanroom-schema)\n\n## Repository Structure\n\n* [examples/](examples/) - example data\n* [project/](project/) - project files (do not edit these)\n* [src/](src/) - source files (edit these)\n    * [cleanroom_schema](src/cleanroom_schema)\n        * [schema](src/cleanroom_schema/schema) -- LinkML schema (edit this)\n* [datamodel](src/cleanroom_schema/datamodel) -- Generated python datamodel\n* [tests](tests/) - python tests\n\n## Developer Documentation\n\n<details>\nUse the `make` command to generate project artefacts:\n\n- `make all`: make everything\n- `make deploy`: deploys site\n\n</details>\n\n## Credits\n\nthis project was made with [linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter)\n',
    'author': 'Mark Andrew Miller',
    'author_email': 'MAM@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
