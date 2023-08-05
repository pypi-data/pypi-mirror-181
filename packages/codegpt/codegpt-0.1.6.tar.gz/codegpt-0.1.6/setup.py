# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codegpt', 'codegpt.commands']

package_data = \
{'': ['*']}

install_requires = \
['nltk>=3.7,<4.0', 'openai>=0.2,<0.3', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['codegpt = codegpt.main:app']}

setup_kwargs = {
    'name': 'codegpt',
    'version': '0.1.6',
    'description': "A CLI tool for refactoring Python code using OpenAI's text-davinci-003 model",
    'long_description': '# Codegpt\n\n## 0.1.5\n\nA tool for using GPT just a little quicker. A nearly truly automated footgun. Learn how to revert with git before trying please.\n\nPosting about progress here:\n\n[![Twitter Follow](https://img.shields.io/twitter/follow/_JohnPartee?style=social)](https://twitter.com/_JohnPartee)\n\n## Getting Started\n\n`pip install codegpt --upgrade`\n\nAnd set your openapi API key as an environment variable like they recommend:\n[In their docs here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)\n\nWindows users can also use `setx` like:\n\n`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`\n\nfrom an admin console.\n\n## Be careful! But try this:\n\nUsage\nTo try Codegpt, you can run the following command:\n\n```bash\ncodegpt todo list <filename>\n```\n\nThis will prompt you for a description of what needs to be done and build a `.todo` file for the filename provided. You can ask it to do whatever, even if you aren\'t sure how to do it (But search to validate its plans, it might bullshit you!). Make sure to mention a technical requirement if you have one, like using a certain module or library. GPT-3 can be pretty lazy if you don\'t get specific.\n\nWhen you start to see good results, you can take the gloves off with:\n\n```bash\ncodegpt todo do <filename>\n```\n\nWhich will attempt to DO the todo list with GPT3\'s help. Results will be mixed. Backup your code first.\n\nOr use the gen command to generate docs.\n\n```bash\ncodegpt gen docs <filename>\n```\n\nFor more advanced (brave? foolhardy?) users, you can use the codegpt unsafe command, which allows you to:\n\nChange variable names to be more readable\n\n```bash\ncodegpt unsafe varnames <filename>\n```\n\nAdd comments to your code automatically\n\n```bash\ncodegpt unsafe comment <filename>\n```\n\nEdit any file\n\n```bash\ncodegpt unsafe edit <filename> "Break this up into smaller functions where you can. Add google style docstrings. Feel free to rewrite any code doesn\'t make sense."\n```\n\nKeep in mind that using GPT-3 for code generation is paid, with a cost of 2 cents per 1,000 tokens.\n\nJust like with a Jr Dev, it\'s best to break up your tasks into smaller pieces to improve the results.\n\nPropose endpoints as issues, I\'ve got a few ideas:\n\n- Write tests for file\n- Generate SQL query from table spec files\n- Generate new file\n',
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
