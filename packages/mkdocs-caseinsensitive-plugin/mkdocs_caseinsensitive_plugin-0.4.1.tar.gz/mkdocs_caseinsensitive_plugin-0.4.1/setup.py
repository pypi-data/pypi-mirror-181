# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_caseinsensitive_plugin']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.4.2,<2.0.0', 'regex>=2022.10.31,<2023.0.0']

entry_points = \
{'mkdocs.plugins': ['caseinsensitivefiles = '
                    'mkdocs_caseinsensitive_plugin:CaseInsensitiveFiles']}

setup_kwargs = {
    'name': 'mkdocs-caseinsensitive-plugin',
    'version': '0.4.1',
    'description': '',
    'long_description': '# mkdocs-caseinsensitive-plugin\n\nThis plugin allows you to link to case-insensitive documentation files.\n\n## Usecase\n\nWhen presented with the following tree directory structure:\n\n```\nproject\n│   works_for_images.md (contains link to "folder1/IMAGE.PNG")\n│   works_for_markdown.md (contains link to "FOLDER1/readme.md")\n│\n└───folder1\n│   │   image.png\n│   │   README.md\n```\n\nMkDocs will produce the following logging warning messages\n\n```\nWARNING  -  Documentation file \'works_for_images.md\' contains a link to \'folder1/IMAGE.PNG\' which is not found in the documentation files.\nWARNING  -  Documentation file \'works_for_markdown.md\' contains a link to \'FOLDER1/readme.md\' which is not found in the documentation files.\n```\n\nConsequently, the rendered HTML files will not have the appropriate links in place.\n\nThis issue has been raised on the [MkDocs repository](https://github.com/mkdocs/mkdocs) before [here](https://github.com/mkdocs/mkdocs/issues/1810). Understandably, this is desirable behaviour due to the differences in operating systems in how lax they are when it comes to case-sensitivity in files and directories.\n\n## Installation\n\nInstall the package with pip:\n\n```bash\npip install mkdocs-caseinsensitive-plugin\n```\n\nTODO:\nInstall the package from source with pip:\n\n```bash\ngit clone https://github.com/TheMythologist/mkdocs-caseinsensitive-plugin.git\n```\n\nEnable the plugin in your `mkdocs.yml`:\n\n```yml\nplugins:\n    - search: {}\n    - caseinsensitive: {}\n```\n\n> **NOTE:** If you have no `plugins` entry in your configuration file yet, you\'ll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.\n',
    'author': 'TheMythologist',
    'author_email': 'leekaixuan2001@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
