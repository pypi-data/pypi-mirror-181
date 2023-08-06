# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastgen',
 'fastgen.apps',
 'fastgen.blocks',
 'fastgen.constants',
 'fastgen.enums',
 'fastgen.exceptions',
 'fastgen.generators',
 'fastgen.managers']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.3', 'rich>=12.5.1,<13.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['fastgen = fastgen.main:app']}

setup_kwargs = {
    'name': 'fastgen',
    'version': '0.3.5',
    'description': 'A CLI for your next FastAPI project',
    'long_description': '<p align="center" class="logo">\n<img src=".\\docs\\logo.png" alt="logo" >\n</p>\n\n<p align="center" class="name">\nFastGen\n</p>\n\n<p align="center" class="slogan"> <em>A CLI for your next FastAPI Project</em></p>\n\n<!-- <style>\n    .slogan{\n        margin-top:-9px;\n        padding-bottom:15px;\n        font-size:15px\n    }\n    .logo{\n        padding-bottom:10px;\n        padding-top:25px\n    }\n    .name{\n      font-size:20px;\n      font-weight:bold\n    }\n</style> -->\n\n---\n\n<!-- # ⚡ _**FastGen**_\n\nStart FastAPI Projects in Lightning Speed.\n\nBuilt With **Typer** To Help With <span style="color:green">**FastAPI**</span>.... -->\n\n## 👀 **Take A Look**\n\nthis is a glanc of the project structure you will have once you use **FastGen**\n\n![dirs_images](./docs/dir.png)\n\n## **Navigate Quickly**\n\n[installation](#✨-installation)<br>\n[commands](#🧭-commands)\n\n- [info](#fastgen-info)\n- [new](#fastgen-new)\n- [g](#fastgen-g)\n\n## ✨ **Installation**\n\nUsing pip :\n\n```console\n$ python -m pip install fastgen\n```\n\nUsing Poetry :\n\n```console\n$ poetry add fastgen\n```\n\n## 🧭 **Commands**\n\n**Usage**:\n\n```console\n$ fastgen [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n- `--install-completion`: Install completion for the current shell.\n- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n- `--help`: Show this message and exit.\n\n**Commands**:\n\n- `info`\n- `new`\n\n## **`fastgen info`**\n\n**Usage**:\n\n```console\n$ fastgen info [OPTIONS]\n```\n\n**Options**:\n\n- `--help`: Show this message and exit.\n\n## **`fastgen new`**\n\n**Usage**:\n\n```console\n$ fastgen new [OPTIONS] ⭐ Project Name\n```\n\n**Arguments**:\n\n- `⭐ Project Name`: <span style="color:pink">**required**\n\n**Options**:\n\n- `--dir 📁 Directory Path`\n- `--package-manager 📦 Package Manager`: [default: pip]\n  ( Options are pip , poetry )\n- `--migrations / --no-migrations`: [default: False]\n- `--docker / --no-docker`: [default: False]\n- `--testing / --no-testing`: [default: False]\n- `--database 📅 Database`: [default: postgresql] ( Options are postgresql,mysql,sqlite )\n- `--orm ⚙️ ORM`: [default: False]\n- `--help`: Show this message and exit.\n\n## **`fastgen g`**\n\n**Usage**:\n\n```console\n$ fastgen g [OPTIONS] <component> <component_name>\n```\n\n**Available Components**\n| Component | In stock |\n|--------------|------------|\n| router | generates new rotuer at app/api/routers |\n| model | generates new sqlmodel or sqlalchemy mode at app/database/models |\n| schema | generates new pydantic schema at app/api/schemas\n\n**Options**\n\n- `--model-type` : available only for model components , optional values are ( sqlmodel , sqlalchemy )\n- `--path` : specifiy where to create the component **RELATIVE TO THE CURRENT WORKING DIRECOTRY** if not in default path\n\n- **Note** : the naming is preferred to be in lower case so it can be resolved correctly\n\n**Arguments**\n\n```console\n\n```\n\n## 🪲 **Encountered A Problem !**\n\nfeel free to open an issue discussing the problem you faced\n\n## 🤝🏻 **Contributing**\n\nplease refer to [Contribution Guide](./CONTRIBUTING.md)\n',
    'author': 'kareem',
    'author_email': 'kareemmahlees@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kareemmahlees/fastgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
