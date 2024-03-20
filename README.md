PyTape
=====

Python wrapper for the Tape API.

Install
-------

Dependencies

* httplib2

Install PyTape by cloning from the GitHub repo:

    $ git clone git://github.com/gentilnegocios/tape-py.git
    $ cp -r tape-py/pytape path/to/destination

Alternatively, install via `pip`:

    $ pip install git+https://github.com/gentilnegocios/tape-py.git#egg=pytape


Example
-------

    from pytape import api
    from client_settings import *

    client = api.BearerClient(user_key)
    print client.Record.find(22342)


Tests
-----

To run tests for the API wrapper, you need two additional dependencies:

* mock
* nose

With those installed, run `nosetests` from the repository's root directory.


Meta
----

* Code: `git clone https://github.com/gentilnegocios/tape-py.git`
* Home: <https://github.com/gentilnegocios/tape-py>
* Bugs: <https://github.com/gentilnegocios/tape-py/issues>
