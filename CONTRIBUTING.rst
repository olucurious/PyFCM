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

Before commiting your changes, please run the tests. For running the tests you need service account credentials in a JSON file.
These do NOT have to be real credentials, but must have a properly encoded private key. You can create a key for testing using a site
like [cryptotools](https://cryptotools.net/rsagen). For example:

```
{
    "type": "service_account",
    "project_id": "splendid-donkey-123",
    "private_key_id": "12345",
    "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMYTESTKEY\n-----END RSA PRIVATE KEY-----",
    "client_email": "firebase-adminsdk@splendid-donkey-123.iam.gserviceaccount.com",
    "client_id": "789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-splendid-donkey-123.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
```


**Please do not use a service account or private key, which is used in production!**

::

    pip install . ".[test]"

    export GOOGLE_APPLICATION_CREDENTIALS="path/to/service_account.json"
    export FCM_TEST_PROJECT_ID="test-project-id"

    python -m pytest

If you add a new fixture or fix a bug, please make sure to write a new unit test. This makes development easier and avoids new bugs.


Branching
---------

There are two main development branches: ``master`` and ``develop``. ``master`` represents the currently released version while ``develop`` is the latest development work. When submitting a pull request, be sure to submit to ``develop``.

