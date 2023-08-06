# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonlocalbox']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1']

setup_kwargs = {
    'name': 'nonlocalbox',
    'version': '0.1',
    'description': 'A friendly API for simulating nonlocal no-signalling correlations',
    'long_description': 'NonlocalBox\n===========\n\n**A friendly API for simulating nonlocal no-signalling correlations.**\n\nInstallation\n------------\n\nThe easiest way to install ``NonlocalBox`` is to use the ``pip`` command:\n\n.. code:: sh\n\n    python -m pip install nonlocalbox\n\nYou may need to replace ``python`` with the correct Python interpreter, e.g., ``python3``.\n\nUsage\n-----\nThe following example illustrates a simple game between Alice and Bob. First, we\nneed to create two instances of ``NonlocalBox``, one for Alice and one for Bob:\n\n.. code:: python\n\n    from os import environ\n    from nonlocalbox import NonlocalBox\n\n    alice_game = NonlocalBox(environ["ALICE_API_KEY"])\n    bob_game = NonlocalBox(environ["BOB_API_KEY"])\n\nIn the current state, neither of them are in any role. Suppose that Alice invites\nBob for a simulation, whose username is known by Alice (which is \'bob\' in this case).\nAlice wants to use Popescu-Rohrlich Box of box ID 1 and names it \'hellothere\':\n\n.. code:: python\n\n    alice_game.invite("bob", 1, \'hellothere\')\n    print(alice_game.box_id)  # this is arbitrary\n    4\n\nIn the server side, Bob is automatically added to this box. They both should\ninitialize the newly created box with ID 4. This will set the role \'Alice\'\nto Alice and \'Bob\' to Bob (since there won\'t be any box in Bob\'s list with ID 4):\n\n.. code:: python\n\n    alice_game.initialize(4)\n    bob_game.initialize(4)\n\nThey can use the nonlocal boxes to run a simulation.\n\nSuppose Alice sends `x = 0` are her input to the box with transaction ID ``20220311001`` and\nBob sends `y = 0` with the same transaction ID. Note that for `x = y = 0` the results should\nbe correlated:\n\n.. code:: python\n\n    print(alice_game.use(0, "20220311001"))\n    0\n    print(bob_game.use(0, "20220311001"))\n    0\n\nNow suppose Bob will be the first to send `y = 1` with an incremented transaction ID, and\nAlice also sends `x = 1`. The results should be anticorrelated:\n\n.. code:: python\n\n    print(bob_game.use(1, "20220311002"))\n    1\n    print(alice_game.use(1, "20220311002"))\n    0\n\n',
    'author': 'Ottó Hanyecz',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ohanyecz/nonlocalbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
