How to Contribute
=================

- Overview_
- Guidelines_
- Branching_


Overview
--------

1. Fork the repo.
2. Improve/fix the code.
3. Write and run tests
4. Add your changes to CHANGES.rst
5. Push to your fork and submit a pull request to the ``develop`` branch.


Guidelines
----------

Some simple guidelines to follow when contributing code:

- Adhere to `PEP8`.
- Clean, well documented code.


Tests
-----

Before commiting your changes, please run the tests. For running the tests you need an FCM API key.

**Please do not use an API key, which is used in production!** 

::

    pip install . ".[test]"

    export FCM_TEST_API_KEY=AAA...

    python -m pytest

If you add a new fixture or fix a bug, please make sure to write a new unit test. This makes development easier and avoids new bugs.


Branching
---------

There are two main development branches: ``master`` and ``develop``. ``master`` represents the currently released version while ``develop`` is the latest development work. When submitting a pull request, be sure to submit to ``develop``.

