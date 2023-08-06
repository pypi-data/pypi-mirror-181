# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['junction',
 'junction.confluence',
 'junction.confluence.api',
 'junction.confluence.models',
 'junction.git',
 'junction.markdown']

package_data = \
{'': ['*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0',
 'Faker>=13.15.1,<14.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click==8.1.3',
 'colorama>=0.4.3,<0.5.0',
 'gitpython>=3.0.5,<4.0.0',
 'markdown-emdash>=0.1.0,<0.2.0',
 'markdown-urlize>=0.2.0,<0.3.0',
 'markdown>=3.0.1,<4.0.0',
 'markdownsubscript>=2.1.1,<3.0.0',
 'markdownsuperscript>=2.1.1,<3.0.0',
 'pyppeteer>=1.0.2,<2.0.0',
 'pytest-mock>=3.8.2,<4.0.0',
 'python-magic==0.4.27',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['junction = junction.cli:main']}

setup_kwargs = {
    'name': 'annalise-confluence-junction',
    'version': '2.0.0',
    'description': 'Publish to and manage Confluence spaces with markdown files tracked in Git.',
    'long_description': '\n# Annalise AI - Confluence Junction\n\nThis project is expanded from (https://github.com/HUU/Junction) \n\n# TO DO\n\n- move away from using a docker image and use a pushlished python package\n- unit tests for everything\n# Running Locally\n\nTo run this locally run docker compose up with the documents and images directory as env vairables\n```sh\nDOCS=<path to docs> IMAGE=<path to images> docker-compose up\n```\n\n# Overview\n\nJunction works by inspecting the changes made on a commit-by-commit basis to your Git repository, and determining what needs to be changed in Confluence to reflect those changes.  Junction (currently) expects to manage the entire [space in Confluence](https://confluence.atlassian.com/doc/spaces-139459.html).  Thus when using Junction you must tell it which Space to target and update.  You must not manually change, create, or modify pages in the target space, or else Junction may be unable to synchronize the state in Git with the state in Confluence.\n\nTo allow mixing code (and other items) with markdown files for Junction in a single repository, you can tell Junction a subpath within your repository that functions as the root e.g. all markdown files will be kept in `docs/`.  All files should end with the `.md` extension.\n\nThe page will gets its title from the file name, and its contents will be translated into Confluence markup.  See [this example for what output looks like in Confluence](#output-example).\n\n# Usage\n\nCollect a set of credentials that Junction will use to login to Confluence.  You will need to create an [API token](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) to use instead of a password.  **I recommend you make a dedicated user account with access permissions limited to the space(s) you want to manage with Junction**.\n\nIn your git repository, create a folder structure and markdown files you would like to publish.  Commit those changes.\n``` bash\n\n.\n├── (your code and other files)\n└── docs/\n    ├── Welcome.md\n    ├── Installation.md\n    └── Advanced Usage\n    |   ├── Airflow.md\n    |   ├── Visual Studio Online.md\n    |   ├── Atlassian Bamboo.md\n    |   └── GitHub Actions.md\n    └── Credits.md\n```\n\n## Images\nImages should be placed inside the `images` directory within a subdirectory that has the same name as the respective file. for the above example the image directory could look like this.\n\n```\n.\n└── images/\n    ├── Welcome/\n        ├── image1.png\n        └── image2.png\n    ├──  Installation/\n        └── image1.png\n    └── Advanced Usage/\n        ├── image1.png\n        ├── image2.png\n        ├── Airflow/\n            └── image1.png\n```\n\n# Mermaid Diagrams\nMermaid diagrams can be included in the markdown but must include the document name in the opening fence:\n\n` ```mermaid filename=<document name>`\n\nsee [here for using mermaid.js in github](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/)',
    'author': 'Lachlan Newman',
    'author_email': 'lachnewman007@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HUU/Junction',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
