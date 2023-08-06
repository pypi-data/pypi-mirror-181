# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rumex', 'rumex.parsing', 'rumex.parsing.state_machine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rumex',
    'version': '0.1.1',
    'description': '',
    'long_description': "=====\nRumex\n=====\n\n`Behaviour Driven Development`_ (BDD) testing library.\n\nRumex is a lightweight library alternative to an existing framework `behave`_.\n\n\nBasic example\n-------------\n\n.. code:: python\n\n\timport rumex\n\n\texample_file = rumex.InputFile(\n\t\ttext='''\n\t\t\tName: Example file\n\n\t\t\tScenario: Simple arithmetics\n\n\t\t\t\tGiven an integer 1\n\t\t\t\tAnd an integer 2\n\t\t\t\tWhen addition is performed\n\t\t\t\tThen the result is 3\n\t\t''',\n\t\turi='in place file, just an example',\n\t)\n\n\tsteps = rumex.StepMapper()\n\n\n\t@steps(r'an integer (\\d+)')\n\tdef store_integer(integer: int, integers=None):\n\t\tintegers = integers or []\n\t\tintegers.append(integer)\n\t\treturn dict(integers=integers)\n\n\n\t@steps(r'addition is performed')\n\tdef add(integers):\n\t\treturn dict(result=sum(integers))\n\n\n\t@steps(r'the result is (\\d+)')\n\tdef check_result(expected_result: int, *, result):\n\t\tassert expected_result == result\n\n\n\trumex.run(\n\t\tfiles=[example_file],\n\t\tsteps=steps,\n\t)\n\n\n.. _`Behaviour Driven Development`:\n  https://en.wikipedia.org/wiki/Behavior-driven_development\n\n.. _`behave`: https://github.com/behave/behave\n",
    'author': 'uigctaw',
    'author_email': 'uigctaw@metadata.social',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
