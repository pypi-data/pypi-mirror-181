# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_toolkit', 'cli_toolkit.tests']

package_data = \
{'': ['*']}

install_requires = \
['sys-toolkit>=2,<3']

entry_points = \
{'pytest11': ['cli_toolkit_fixtures = cli_toolkit.fixtures']}

setup_kwargs = {
    'name': 'cli-toolkit',
    'version': '2.3.0',
    'description': 'Classes to implement CLI commands in python',
    'long_description': '![Unit Tests](https://github.com/hile/cli-toolkit/actions/workflows/unittest.yml/badge.svg)\n![Style Checks](https://github.com/hile/cli-toolkit/actions/workflows/lint.yml/badge.svg)\n\n# CLI toolkit for shell command utilities\n\nThis module contains modules to implement CLI scripts by wrapping\npython argparse.ArgumentParser to user friendly utility classes.\n\n## Create a script class\n\nMain class to use is the Script class. It will get it\'s name from\nsys.argv[0].\n\nExample:\n\n```python\nfrom cli_toolkit.script import Script\n\nif __name__ == \'__main__\':\n    script = Script()\n    script.add_argument(\'files\', nargs=\'*\', help=\'Files to process\')\n    args = script.parse_args()\n    for filename in args.files:\n        script.debug(\'PROCESSING\', filename)\n        script.message(filename)\n```\n\nRunning the example:\n\n```\n> python test.py foo bar\nfoo\nbar\n```\n\nThis is pretty straightforward ArgumentParser, except it\n\n* sets SIGINT handler\n* adds --debug and --quiet flags\n* adds `debug` and `message` functions which honor the debug and quiet flags\n\n## Using script with subcommands\n\nMore useful is using a script with subcommands. The subcommands require\nat least `name` class variable and should have `usage`, `description` and\n`epilog`.\n\nYou also should implement `run` method and call script.run() to run correct\nsubcommand. Arguments for subcommand parser are registered with method\n`register_parser_arguments`.\n\n```python\nfrom cli_toolkit.script import Script\nfrom cli_toolkit.command import Command\n\n\nclass ListCommand(Command):\n    name = \'list\'\n    usage = \'List files\'\n    description = \'Lists files specified on command line\'\n\n    def register_parser_arguments(self, parser):\n        parser.add_argument(\'files\', nargs=\'*\', help=\'Files to process\')\n\n    def run(self, args):\n        for filename in args.files:\n            self.debug(\'PROCESSING\', filename)\n            self.message(filename)\n\n\nif __name__ == \'__main__\':\n    script = Script()\n    script.add_subcommand(ListCommand(script))\n    script.run()\n```\n\nRunning the example:\n\n```bash\n> python test.py list foo bar\nfoo\nbar\n```\n\n## Using nested subcommands\n\nThe subcommands can be nested. You need to pass the parser in paren\'t\nregister_parser_subcommand to add_subcommand.\n\n```python\nfrom cli_toolkit.script import Script\nfrom cli_toolkit.command import Command\n\n\nclass FilesCommand(Command):\n    name = \'demo\'\n    usage = \'Run nested demo subcommands\'\n\n    def register_parser_arguments(self, parser):\n        """\n        Register \'list\' command under demo subcommand\n        """\n        self.add_subcommand(ListCommand(self), parser)\n        return parser\n\n\nclass ListCommand(Command):\n    name = \'list\'\n    usage = \'List files\'\n    description = \'Lists files specified on command line\'\n\n    def register_parser_arguments(self, parser):\n        """\n        Register \'list\' command arguments\n        """\n        parser.add_argument(\'files\', nargs=\'*\', help=\'Files to process\')\n        return parser\n\n    def run(self, args):\n        if not args.files:\n            self.exit(1, \'No files provided\')\n        for filename in args.files:\n            self.debug(\'PROCESSING\', filename)\n            self.message(filename)\n\n\nif __name__ == \'__main__\':\n    script = Script()\n    script.add_subcommand(FilesCommand(script))\n    script.run()\n```\n\nRunning the example:\n\n```bash\n> python test.py demo list foo bar\nfoo\nbar\n```\n',
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
