# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sourcery_rules_generator', 'sourcery_rules_generator.cli']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'typer[all]==0.7.0']

entry_points = \
{'console_scripts': ['sourcery-rules = sourcery_rules_generator.cli.cli:app']}

setup_kwargs = {
    'name': 'sourcery-rules-generator',
    'version': '0.3.1',
    'description': 'Generate architecture rules for Python projects.',
    'long_description': '# Sourcery Rules Generator \n\n**This is an experimental project. It might become a part of the [Sourcery CLI](https://docs.sourcery.ai/Overview/Products/Command-Line/).**\n\nSourcery Rules Generator creates architecture rules for your project.\n\nThe generated rules can be used by Sourcery to review your project\'s architecture.\n\nCurrently, the project can create dependency rules.\n\n## Usage\n\nYou can create Sourcery rules based on a template with the command:\n\n```\nsourcery-rules <TEMPLATE-NAME> create\n```\n\nSupported templates:\n\n* dependencies\n* naming (coming soon)\n\nFor example:\n\n```\nsourcery-rules dependencies create\n```\n\n![gif sourcery-rules dependencies create](https://raw.githubusercontent.com/sourcery-ai/sourcery-rules-generator/main/sourcery-rules_dependencies_create.gif)\n\n### Create Dependencies Rules\n\nWith the dependencies template, you can create rules to check the dependencies:\n\n* between the packages of your application\n* to external packages.\n\nLet\'s say your project has an architecture like this:\n\n![dependencies overview](https://raw.githubusercontent.com/sourcery-ai/sourcery-rules-generator/main/dependencies.png)\n\nYou can create rules to ensure:\n\n* no other package imports `api`\n* only `api` imports `core`\n* only `db` import `SQLAlchemy`\n* etc.\n\nRun the command:\n\n```\nsourcery-rules dependencies create\n```\n\nYou\'ll be prompted to provide:\n\n* a package name\n* the packages that are allowed to import the package above\n\nThe 2nd parameter is optional.  \nE.g. it makes sense to say that no other package should import the `api` or `cli` package of your project.\n\n=>\n\n2 rules will be generated:\n\n* 1 for `import` statements\n* 1 for `from ... import` statements\n\n## Dependencies Use Cases\n\n### Internal Dependencies Between the Packages of a Project\n\n* [Law of Demeter](https://en.wikipedia.org/wiki/Law_of_Demeter): Packages should talk only to their "direct neighbors".\n* A mature package shouldn\'t depend on a less mature package\n* A core package shouldn\'t depend on a customer-specific package\n\nThanks to [w_t_payne](https://news.ycombinator.com/user?id=w_t_payne) and [hbrn](https://news.ycombinator.com/user?id=hbrn) for their input in this [HackerNews discussion](https://news.ycombinator.com/item?id=33999191#34001608) 😃\n\n### External Dependencies\n\n* [Gateway pattern](https://martinfowler.com/articles/gateway-pattern.html): Ensure that only a dedicated package of your software communicates with an external dependency.\n* Ensure that a deprecated library isn\'t used\n\nThis [blog post](https://sourcery.ai/blog/dependency-rules/) shows a 3-step method of defining dependency rules:\n\n1. Draw a diagram showing the optimal dependencies between your packages.\n2. Phrase some rules in a human language based on the diagram: Which package should depend on which?\n3. Translate the rules into code with Sourcery Rules Generator.\n\n## Using the Generated Rules\n\nThe generated rules can be used by Sourcery to review your project.\nIf you copy the generated rules into your project\'s `.sourcery.yaml`, Sourcery will use them automatically.\n\nAll the generated rules have the tag `architecture`. Once you\'ve copied them to your `.sourcery.yaml`, you can run them with:\n\n```\nsourcery review --enable architecture .\n```',
    'author': 'reka',
    'author_email': 'reka@sourcery.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sourcery-ai/sourcery-rules-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
