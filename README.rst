LecToCal
========

Lectocal is a python utility for synchronizing schedules from Lectio_ into
`Google Calendar`_. It allows students and teachers of any institution using
lectio, to see their schedules in a calendar platform they may already
be using.

Ultimately the purpose is to make it easier for members of
institutions using lectio to stay on top of their schedules, by allowing
the use of features such as email notifications, and push notifications
on Android and iOS devices, together with the lectio schedule.

.. _Lectio: https://www.lectio.dk/
.. _`Google Calendar`: https://calendar.google.com/

Installation
------------

The source files for lectocal can be downloaded directly from the
`GitHub Repository`_, if you wish to work with the source code, feel free
to download it there.

The recommended installation method for normal use is however through pip,
as this will take care of installing any dependencies necessary,
and install the modules directly used by the end user as executables.

To install using pip run:

::

    pip install lectocal

For more details on using pip, see `Installing Packages`_ by the
Python Packaging Authority.

.. _`GitHub Repository`: https://github.com/Hanse00/LecToCal
.. _`Installing Packages`: http://python-packaging-user-guide.readthedocs.org/en/latest/installing/

Usage
-----

Dependencies
............

lectocal has a number of dependencies, if installed through pip these will
be handled automatically, otherwise they must manually be installed.

As with lectocal, it is recommended these are installed through pip.

Lectocal has the following dependencies:

- google-api-python-client
- requests
- lxml
- pytz
- python-dateutil

They can be installed through pip with:

::

    pip install google-api-python-client requests lxml pytz python-dateutil

Invoking the modules
....................

Once you have lectocal installed (preferably through pip), there's a number of
ways to invoke the two modules you'll primarily be using:

- run.py
- gauth.py

The modules can either be executed as python files:

::

    python run.py
    python gauth.py

They can also be fed to python as modules:

::

    python -m run
    python -m gauth

Finally, if the package was installed by setuptools (This is done automatically
by pip) two executable scrips will be generated:

::

    lectocal.run
    lectocal.gauth

(Native executable .exe files should be generated on Windows systems)

Parameters
..........

A number of parameters are supported when running the run and gauth modules.
The current list can always be seen by running the modules with the ``-h`` flag.
As such:

::

    python run.py -h
    python -m run -h
    lectocal.run -h

How to use
..........

Using lectocal consists of two distinct steps, of which the first should
only be required once, and the second can be repeated to update the calendar.

Step 1
::::::

Generating the user OAuth credentials.

Before it's possible to start reading and writing data to the user's Google
Calendar, we must obtain OAuth credentials authorizing the package to interact
with it.

This is done by running the ``gauth`` module, which will use the client secret
file provided with the package, together with the user authenticating through
a web browser, to generate a credentials file.

See ``gauth -h`` for a list of possible parameters, however the default values
should be acceptable in most usecases.

After the credentials file has been obtained, it can be used to sync the schedules.

Step 2
::::::

Synchronizing Lectio schedule to Google Calendar.

With the credentials file, we are authorized to interact with the user's
Google Calendar. We can therefore now run the ``run`` module, to scrape the
Lectio schedule, and write it into Google Calendar.

If you're running the ``run`` module for the first time for a given user,
the full schedule will simply be copied over. On every subsequent invocation
of the module, it will determine which, if any, lessons have changed since the
last schedule sync, and update those with the new data.

The ``run`` module takes 3 positional arguments, which are required to run
the module. Other arguments can be seen with ``run -h``, however the defaults
for there should suffice in most cases.

The positional arguments are:

::

    run school_id user_type user_id

- school_id
    This is the id number of the school, at which the user is a member,
    in Lectio's system.

    It can be found by browsing to your school's front page (eg.
    https://www.lectio.dk/lectio/523/default.aspx), the school id is the number
    in the page URL, in my case 523.

- user_type
    The user type can take one of two values, depending on if the user
    you are trying to sync schedules for, is registered as a teacher or a
    student in Lectio.

    The possible values are: ``student`` and ``teacher``.

- user_id
    This is the id number of a user within a given school, in lectio these
    are known as elevid or laererid depending on which type the user has.
    Both of these id types are used as user_id in lectocal.

    To find the id of a user, open their schedule page (eg.
    https://www.lectio.dk/lectio/523/SkemaNy.aspx?type=elev&elevid=2486079338)
    the user id number, is the number behind elevid= or laererid= depending
    on the user type, in this case 2486079338.

Invoking the script will therefor look like this:

::

    run 523 student 2486079338

Note
....

The automatically generated calendar in Google Calendar should not be manually
edited. Editing in this calendar may either cause lectocal to remove your
changes, or behave in other unexpected ways.

License
-------
LecToCal is licensed under the Apache 2.0 license, see LICENSE_ or
apache.org_ for details.

.. _LICENSE: LICENSE
.. _apache.org: http://www.apache.org/licenses/LICENSE-2.0
