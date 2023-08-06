# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['def_main']
setup_kwargs = {
    'name': 'def-main',
    'version': '0.11.0',
    'description': 'Define the main function in one step and make it testable',
    'long_description': "========================================================\n``def_main``: a tiny decorator to define main\n========================================================\n\nDefine the main function in one step.\n\nFor any non-trivial projects, use typer and dtyper instead!\n\n\nUsage example\n==================\n\nWithout an return code\n~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n    import def_main\n\n    @def_main\n    def main(*argv):\n        print('hello,', *argv)\n\n\nmeans precisely the same as:\n\n.. code-block:: python\n\n    def main(*argv):\n        print('hello,', *argv)\n\n\n    if __name__ == '__main__':\n        import sys\n\n        main(sys.argv[1:])\n\nWith a return code\n~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code-block:: python\n\n\n    import def_main\n\n    @def_main\n    def main(*argv):\n        print('hello,', *argv)\n        return argv\n\n\nmeans precisely the same as:\n\n.. code-block:: python\n\n    def main(*argv):\n        print('hello,', *argv)\n        return argv\n\n\n    if __name__ == '__main__':\n        import sys\n\n        returncode = main(sys.argv[1:])\n        sys.exit(returncode)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
