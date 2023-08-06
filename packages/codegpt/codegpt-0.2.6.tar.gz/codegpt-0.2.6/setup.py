# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codegpt']

package_data = \
{'': ['*']}

install_requires = \
['nltk>=3.7,<4.0', 'openai>=0.2,<0.3', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['codegpt = codegpt.main:app']}

setup_kwargs = {
    'name': 'codegpt',
    'version': '0.2.6',
    'description': "A CLI tool for refactoring code using OpenAI's models",
    'long_description': '# Codegpt\n\n## 0.2.0\n\nA tool for using GPT just a little quicker. A nearly truly automated footgun. Learn how to revert with git before trying please.\n\nPosting about progress here:\n\n[![Twitter Follow](https://img.shields.io/twitter/follow/_JohnPartee?style=social)](https://twitter.com/_JohnPartee)\n\n## Getting Started\n\n`pip install codegpt --upgrade`\n\nAnd set your openapi API key as an environment variable like they recommend:\n[In their docs here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)\n\nWindows users can also use `setx` like:\n\n`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`\n\nfrom an admin console.\n\n## Be careful! But try this\n\nUsage\nTo try Codegpt, you can run the following command:\n\n```bash\ncodegpt do <filenames>\n```\n\nIt will prompt you for directions to follow, and it\'ll do whatever you want. Write new docs, add comments to code, just make sure to ask it to "edit" or "comment" or whatever so it knows to change files or not.\n\nOr use the quick command to do some neat stuff, like:\n\nGenerate docs\n\n```bash\ncodegpt quick docs <filenames>\n```\n\nChange variable names to be more readable\n\n```bash\ncodegpt quick varnames <filenames>\n```\n\nAdd comments to your code automatically\n\n```bash\ncodegpt quick comment <filenames>\n```\n\nCheck for bugs (iffy, but worth a shot)\n\n```bash\ncodegpt quick bugs <filenames>\n```\n\nCheck for vulnerabilities (even more iffy, but worth a shot)\n\n```bash\ncodegpt quick vulns <filenames>\n```\n\nTry to make code less miserable\n\n```bash\ncodegpt quick ugh <filenames>\n```\n\nKeep in mind that using GPT-3 for code generation is paid, with a cost of 2 cents per 1,000 tokens.\n\nJust like with a Jr Dev, it\'s best to break up your tasks into smaller pieces to improve the results.\n\nPropose endpoints as issues, I\'ve got a few ideas:\n\n- Write tests for file\n- Generate SQL query from table spec files\n- Generate new file\n',
    'author': 'John Partee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/morganpartee/codegpt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
