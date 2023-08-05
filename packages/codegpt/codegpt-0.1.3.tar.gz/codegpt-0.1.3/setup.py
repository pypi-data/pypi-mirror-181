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
    'version': '0.1.3',
    'description': "A CLI tool for refactoring Python code using OpenAI's text-davinci-003 model",
    'long_description': '# Codegpt\n\nA tool for using GPT just a little quicker. A nearly truly automated footgun. Learn how to revert with git before trying please.\n\nPosting about progress here:\n\n[![Twitter Follow](https://img.shields.io/twitter/follow/_JohnPartee?style=social)](https://twitter.com/_JohnPartee)\n\n# Getting Started\n\n`pip install codegpt`\n\nAnd set your openapi API key as an environment variable like they recommend:\n[In their docs here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)\n\nWindows users can also use `setx` like:\n\n`$ setx OPENAI_SECRET_KEY=<YOUR_API_KEY>`\n\nfrom an admin console.\n\n## Be careful! But let\'s go.\n\n### Now with 10% less footgun!\n\nTry this new command to see how it works:\n\n`codegpt todo do app.py`\n\nIt\'ll prompt you for what needs done, and give you an option to edit the todo list before we attempt to refactor it.\n\n### The rest\n\nThe fun stuff is in the `unsafe` command.\n\nFind a file you hate (Back it up! Don\'t do it live!) and give it a shot.\n\n`codegpt unsafe edit .\\helper.py "Break this up into smaller functions where you can. Add google style docstrings. Feel free to rewrite any code doesn\'t make sense."`\n\nYou\'ll see something like:\n\n```sh\nThis prompt is 254 tokens, are you sure you want to continue?\nThe most GPT-3 can return in response is 3843. [y/N]: y\n\n(and after a short wait...)\n\nExplanation: The code has been refactored into smaller functions to improve readability, and Google style docstrings have been added.\n```\n\nOther things to try:\n\n- `codegpt unsafe edit` - Try it with anything. Markdown blog posts, js, yaml, python, whatever.\n- `codegpt unsafe varnames` - Changes variable names (and supposed to only be variable names...) to be readable\n- `codegpt unsafe comment` - Automatically add comments to a file.\n\nPropose endpoints as issues, I\'ve got a few ideas:\n\n- Explain file\n- Write tests for file\n- Generate SQL query from table spec files\n- Generate new file\n- Generate documentation from a file\n\nJust remember this is paid - 2 cents per 1k tokens is a lot when you\'re working on files with a few hundred lines.\n\nAnd remember to break up what you\'re working on - Results will be better with less moving parts and things to do.\n',
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
