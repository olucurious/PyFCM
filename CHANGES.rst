.. _changelog:

Changelog
=========

v0.0.1 (05-06-2016)
-------------------

- First release.

.. _Emmanuel Adegbite: https://github.com/olucurious


v0.0.2 (07-06-2016)
-------------------

- Added topic messaging functionality.

.. _Emmanuel Adegbite: https://github.com/olucurious


v0.0.3 (08-06-2016)
-------------------

- changes in README.rst

.. _Emmanuel Adegbite: https://github.com/olucurious

v0.0.4 (09-06-2016)
-------------------

- Fixed "registration_id of notify_single_device does not work with a str input"

.. _Emmanuel Adegbite: https://github.com/olucurious

v0.0.5 (22-06-2016)
-------------------

- Fixed python 3 import issue

.. _MrLucasCardoso: https://github.com/MrLucasCardoso

v0.0.6 (23-06-2016)
-------------------

- Fixed xrange issue in python3

.. _Emmanuel Adegbite: https://github.com/olucurious

v0.0.7 (24-06-2016)
-------------------

- Added support for sending data only messages

.. _Emmanuel Adegbite: https://github.com/olucurious

v0.0.8 (26-06-2016)
-------------------

- Checking content-length in response.headers, otherwise it will crash, when calling response.json()

.. _Rishabh : https://gihub.com/elpoisterio

v1.0.0 (12-07-2016)
-------------------

- Added proxy support, more fcm arguments and bump version to 1.0.0

.. _Emmanuel Adegbite: https://github.com/olucurious

v1.0.0 (16-07-2016)
-------------------

- Added extra_kwargs for dinamic vars in notify_single_device/notify_multiple_devices functions

.. _Sergey Afonin: https://github.com/safonin

v1.0.1 (04-08-2016)
-------------------

- Added tornado support

.. _Dmitry Nazarov: https://github.com/mkn8rd

v1.1.4 (11-11-2016)
-------------------

- added body_loc_key support and notify single device single response

.. _Emmanuel Adegbite: https://github.com/olucurious

v1.1.5 (16-11-2016)
-------------------

- Fix some message components not being sent if message_body is None (click_action, badge, sound, etc)

.. _João Ricardo Lourenço: https://github.com/Jorl17

v1.2.0 (16-11-2016)
-------------------

- Updated response retrieval, notify_single_device response returns single dict while notify_multiple_devices returns a list of dicts
- You can now pass extra argument by passing it as key value in a dictionary as extra_kwargs to any notification sending method you want to use
- It is now possible to send a notification without setting body or content available

.. _Emmanuel Adegbite: https://github.com/olucurious

v1.2.3 (09-02-2017)
-------------------

- Added support for checking for and returning valid registration ids, useful for cleaning up database

.. _baali: https://github.com/baali


v1.2.9 (07-04-2017)
-------------------

- Fixed issue with notification extra kwargs

.. _Emmanuel Adegbite: https://github.com/olucurious

Unreleased
-------------------

- Add optional json_encoder argument to BaseAPI to allow configuring the JSONEncoder used for parse_payload

.. _Carlos Arrastia: https://github.com/carrasti

- Addition of a android dictionary to set fcm priority

.. _Pratik Sayare: https://github.com/gizmopratik

- Add android_channel_id

.. _Lucas Hild: https://github.com/Lanseuo

- Add configurable retries to info endpoint

.. _Christy O'Reilly: https://github.com/c-oreills

- Fix time_to_live check to allow 0

.. _Stephen Kwong: https://github.com/skwong2

- Add pycharm and vscode to gitignore

.. _Alexandr Sukhryn: https://github.com/alexsukhrin

- Fix CONTRIBUTING.rst

.. _Alexandr Sukhryn: https://github.com/alexsukhrin

- Replace deprecated urllib3.Retry options

.. _Frederico Jordan: https://github.com/fredericojordan

- Replace deprecated urllib3.Retry options v2

.. _Łukasz Rogowski: https://github.com/Rogalek
