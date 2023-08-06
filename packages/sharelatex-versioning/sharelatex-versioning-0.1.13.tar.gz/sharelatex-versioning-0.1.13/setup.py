# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sharelatex_versioning',
 'sharelatex_versioning.classes',
 'sharelatex_versioning.logic',
 'sharelatex_versioning.tests',
 'sharelatex_versioning.tests.rsc',
 'sharelatex_versioning.utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'keyring>=23.11.0,<24.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['sharelatex-versioning = sharelatex_versioning.main:app']}

setup_kwargs = {
    'name': 'sharelatex-versioning',
    'version': '0.1.13',
    'description': 'Tool to backup ShareLaTeX files locally.',
    'long_description': '# ShareLaTeX-Versioning\n\nThe idea of this repository is pretty simple.\nYou are writing your paper using [TUM\'s ShareLaTeX instance](https://sharelatex.tum.de).\nAlthough ShareLaTeX is cool, you also want to have your paper under git version control.\nHere, this tool comes into play.\nWith this tool, you can download and extract your project with one command.\nAll the extracted files are automatically marked as read-only so that you are not tempted to directly modify them on your local hard drive.\nIf you want, you can instruct the script to delete all files which are no longer part of your ShareLaTeX project.\nThis is especially handy when you delete files in ShareLaTeX and you want them also deleted in your git repository.\n\n## General Setup\n\n1. Install [Python](https://www.python.org/downloads/)\n2. Install the package\n\n    ```bash\n    pip install sharelatex-versioning\n    ```\n\n    Now you should be able to call `sharelatex-versioning` within your shell.\n\n    **Attention**: On macOS, `pip` is usually the installer of the Python2 instance.\n    Please use `pip3` or `pip3.x` in this case.\n\n## Repository Setup\n\n1. Open your ShareLaTeX project.\n5. In the URL field of your browser, the link of your project should look like this.\n\n    ```bash\n   https://sharelatex.tum.de/project/this-is-your-project-id\n    ```\n\n   Note the `project_id`\n6. Create folder named `my_cool_sharelatex_project`\n7. Change the directory into the folder\n8. Initialize a git repository\n\n    ```bash\n    git init\n    ```\n\n9. Create a file named `sv_config.json`\n10. Open that file and change it to\n\n    ```json\n    {\n        "project_id": "your_project_id",\n        "username": "your LRZ ID",\n        "sharelatex_url": "https://sharelatex.tum.de/"\n    }\n    ```\n\n    Replace the placeholders with your values.\n11. Store the password in the password manager using [keyring](https://pypi.org/project/keyring/).\n\n   ```bash\n   sharelatex-versioning store-password-in-password-manager --user_name "your LRZ ID" --password "your password"\n   ```\n\n   Afterward, the password should be in the password manager, e.g., in the Keychain on macOS.\n   For deleting the password again, c.f. [here](#store-password-in-password-manager).\n\n## Creating a commit\n\n1. Run the command\n\n    ```bash\n    sharelatex-versioning download-zip --in_file ./sv_config.json\n    ```\n\n    Now, you should have a local copy of your ShareLaTeX project.\n3. Commit your changes\n\n## Cron\n\nYou can also use this tool within a cron job to create every X minute a new commit.\n\n1. Create script file, e.g., `commit.sh`\n2. Make it executable\n\n    ```bash\n    chmod +x commit.sh\n    ```\n\n3. Change the content to the following\n\n    ```bash\n    sharelatex-versioning download-zip --in_file /path/to/sv_config.json --working_dir /path/to/repository\n    cd /path/to/repository\n    git commit -m "Update"\n    ```\n\n   Usually, it is better to use the absolute path to the `sharelatex-versioning` script.\n   You can get this path by calling\n\n   ```bash\n   which sharelatex-versioning\n   ```\n\n4. Open cron\n\n    ```bash\n    crontab -e\n    ```\n\n5. Add this line\n\n   ```cron\n   1/10  8-18    *       *       1-5             /path/to/commit.sh >> /path/to/repo/commit.log 2>&1\n   ```\n\n    Now, every 10 minute, there will be a commit with the new changes to your ShareLaTeX project.\n\n## Command line usage\n\n```bash\nsharelatex-versioning --help\nUsage: sharelatex-versioning [OPTIONS] COMMAND [ARGS]...\n\n  :return:\n\nOptions:\n  --version  Version\n  --help     Show this message and exit.\n\nCommands:\n  download-zip                    This command downloads your ShareLaTeX...\n  store-password-in-password-manager\n                                  Stores the password in the password...\n```\n\n### Download ZIP\n\n```bash\nsharelatex-versioning download-zip --help\nUsage: sharelatex-versioning download-zip [OPTIONS]\n\n  This command downloads your ShareLaTeX project as ZIP compressed file.\n  Next, the zip folder is extracted into the current directory. All files\n  are made readonly as the local repository should not be the place to edit\n  the files. If you want, the script can also delete all the files which are\n  no longer in your project. Thus, files deleted on the ShareLaTeX instance\n  are also deleted locally.\n\nOptions:\n  -f, --force             If this flag is passed, all the files which are not\n                          part of the ShareLaTeX project and not covered by\n                          .gitignore or the white_list option, are deleted.\n\n  -i, --in_file TEXT      The path of a JSON file containing the information\n                          of the ShareLaTeX project.\n\n  -w, --white_list TEXT   The path of a file containing all the files which\n                          are not part of the ShareLaTeX project, but should\n                          not be deleted. You can use UNIX patterns.\n\n  -d, --working_dir TEXT  The path of the working dir\n  --help                  Show this message and exit.\n```\n\n### Store Password In Password Manager\n\n```bash\nsharelatex-versioning store-password-in-password-manager --help\nUsage: sharelatex-versioning store-password-in-password-manager\n           [OPTIONS]\n\n  Stores the password in the password manager.\n\nOptions:\n  -f, --force           If true, we will overwrite existing passwords.\n  -p, --password TEXT   The password for the Overleaf/ShareLaTex instance.\n  -u, --user_name TEXT  The username\n  --help                Show this message and exit.\n```\n\nIn case, you want to delete the password again, you can use the [Windows Credential Manager](https://kb.intermedia.net/Article/44527) or [Keychain](https://www.wikihow.com/Delete-Saved-Passwords-from-the-iCloud-Keychain-on-macOS).\n\n#### Store Password In Password Manager: Example\n\n```bash\nsharelatex-versioning store-password-in-password-manager --user_name "your LRZ ID" --password "your password"\n```\n\n## Contact\n\nIf you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@posteo.de).\n',
    'author': 'Patrick Stöckle',
    'author_email': 'patrick.stoeckle@posteo.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@posteo.de',
    'url': 'https://github.com/pstoeckle/ShareLaTeX-Versioning.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
