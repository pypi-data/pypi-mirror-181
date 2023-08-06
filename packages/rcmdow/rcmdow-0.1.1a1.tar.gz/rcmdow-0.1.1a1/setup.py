# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcmdow', 'rcmdow.core', 'rcmdow.core.display']

package_data = \
{'': ['*']}

install_requires = \
['polars>=0.15.6,<0.16.0',
 'psutil>=5.9.4,<6.0.0',
 'pywin32>=305,<306',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['rcmdow = rcmdow.main:app']}

setup_kwargs = {
    'name': 'rcmdow',
    'version': '0.1.1a1',
    'description': 'A rich python wrapper on the CMDOW window util',
    'long_description': "# Welcome to my rich CMDOW cli\n\nThe CMDOW cli is a command line interface for the CMDOW tool. It is written in python and is a work in progress.\n\n## The CMDOW cli\n\nThe goal is to make a command line interface for CMDOW that is easy to use and has a rich feature set.\nTo avoid python's (and [pandas'](https://pandas.pydata.org/) overhead, [the cli uses polars](https://github.com/pola-rs/polars) to do the heavy lifting.\n\n## The CMDOW tool\n\nCMDOW is a command line tool for Windows that allows you to control windows. It is written in C++ and is available on [the author's webpage.](https://ritchielawrence.github.io/cmdow/)\n\n### Why use CMDOW?\n\nI just stumbled upon CMDOW and I think it is a great tool. It is very powerful and allows you to do a lot of smart stuff with regards to windows. As a humble side project, I decided to write a command line interface for CMDOW that is easy to use and has a rich feature set.\n\nFor example, CMDOW allows you to do the following:\n\nGet a list of all windows and their positions/sizes (in pixels):\n\n```powershell\ncmdow /p /f\n```\n\nHowever the output was pure text, and I wanted to add a little bit of spark to it. So I wrote a python script that uses [polars](https://github.com/pola-rs/polars) to parse the output and make it a bit more readable. You can get the same output as above by running the following command:\n\n```powershell\nrcmdow raw\n```\n\nNote that the `raw` command is just an alias for `cmdow /p /f`.\nTo add a little bit of spark to the output, you can run the following command:\n\n```powershell\nrcmdow ls\n```\n\nThis will give you a nice table with the windows and their positions/sizes.\n\n## Features / Usage\n\n### Get information about windows\n\nThe equivalent of `cmdow /t /p /f` (which lists only taskbar windows) can be achieved by running the following command:\n\n```powershell\nrcmdow lst\n```\n\nTo let the cli tool guess what your current layout is, run the following command:\n\n```powershell\nrcmdow layout\n```\n\nThis output is just a filter on top of the `rcmdow ls` command. It will show you all windows that are visible on your screen.\n\n### Move windows\n\nSo far the cli tool only supports screen splitting. You can split your screen into two halves by running the following command:\n\nLeft/Right:\n\n```powershell\nrcmdow hzl name1 name2\n```\n\nYou can get the names of the windows by running the `rcmdow ls` or `rcmdow lst` command and selecting the `Image` column.\nNote that the names are **not case sensitive.**\n\nTop/Bottom:\n\n```powershell\nrcmdow vtl name1 name2\n```\n\n## Installation\n\n### Prerequisites\n\n- Python 3.8 or higher\n- The CMDOW tool (available [here](https://ritchielawrence.github.io/cmdow/))\n\n### An easy way to install\n\nI recommend using [scoop](https://scoop.sh/) to install the CMDOW cli. It is a command line installer for Windows that makes installing and updating software a breeze.\n\nTo install scoop, run the following command in powershell:\n\n```powershell\nSet-ExecutionPolicy RemoteSigned -Scope CurrentUser # Optional: Needed to run a remote script the first time\nirm get.scoop.sh | iex\n```\n\nTo install the CMDOW cli, run the following command in powershell:\n\n```powershell\nscoop bucket add extras\nscoop install cmdow\n```\n\n**Note:** The cli tool assumes you can call cmdow from the command line. If you installed CMDOW to a different location, you will have to add the location to your PATH variable.",
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arnos-stuff/cmdow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
