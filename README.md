# Lectocal

[![CircleCI](https://circleci.com/gh/Hanse00/LecToCal.svg?style=svg)](https://circleci.com/gh/Hanse00/LecToCal)
[![Coverage Status](https://coveralls.io/repos/github/Hanse00/LecToCal/badge.svg?branch=master)](https://coveralls.io/github/Hanse00/LecToCal)

Lectocal is a python module for syncronizing Lectio schedules into Google Calendar.

By leveraging the Google Calendar backend, it can provide: Notifications, Sharing, Access across most devices, integration with other services such as [If This Then That](https://ifttt.com).

## Development

So you want to work with the code? Awesome!

This project uses [Pipenv](https://pipenv.readthedocs.io/en/latest/), after cloning the repo, do the following:

1. Make sure you have python 3 installed.
2. Create a pipenv in your working directory with `pipenv --three`.
3. Install both the default and development packages from the Pipfile with `pipenv install --dev`.

You should now be ready to work.

For more information on pipenv check out [the documentation](https://pipenv.readthedocs.io/en/latest/). If you run into any issues working with the project, feel free to [open an issue on GitHub](https://github.com/Hanse00/LecToCal/issues).

## Installation

Installation is easiest using pip, as Lectocal is availble on Pypi as a package (http://pypi.org/project/lectocal/). Simply run `pip install lectocal`.

For more details on using pip, check out [the official documentation](https://packaging.python.org/tutorials/installing-packages/).

Alternatively the source code can be downloaded straight from GitHub, using the "Clone or download" button in the top right.

## Usage

### Dependencies

If the package is installed via pip, dependencies will be handled automatically.

Otherwise, these dependencies will need to be downloaded manually - We recommend using [pipenv](https://docs.pipenv.org) and installing the packages as listed in the [Pipfile](Pipfile).

### Invocation

After installation, the module can be invoced with:

```
python -m lectocal.gauth
python -m lectocal.run
```

If installed via setuptools (pip does this) two executables will also be generated:
```
lectocal.gauth
lectocal.run
```

These can be executed by the system directly.

### Parameters

For all the parameters supported, run the intended module with the -h or --help parameters.

### Example use

1. Generating Calendar OAuth credentials.

    The first step is to generate OAuth credentials for the Google account, to which the schedule must be written.

    This is done by running `lectocal.gauth`, and following the steps in the browser. 

    These steps authorize lectocal to get a credential which gives full calendar access, so new events can be written, and old ones deleted.

1. Syncronizing the schedule.

    After the OAuth credential exists, Lectocal can now write into the calendar using the API.

    Running `lectocal.run` at this point, scrapes the schedule for the chosen individual, and writes it to the calendar.

1. Repeat.

    To keep a calendar up to date, step 2 will need to be repeated at a given interval.
    This can for example be done using cron, or a similar task scheduling system.

    As long as the OAuth credentials are not deleted from the system, or revoked from the Google account, step 1 should not need to be re-run.

**Note**

The generated Google Calendar should not be deleted or renamed, this may cause the system to break, or act in unexpected ways, such as creating a duplicate calendar.

## Bugs, Feedback, Thoughts, etc.

For bugs, issues, or questions about the software, use the [issue tracker built into GitHub](https://github.com/Hanse00/LecToCal/issues).

For general discussion, feedback, etc. there's a mailgroup at [lectocal@googlegroups.com](https://groups.google.com/forum/#!forum/lectocal).

## License

Lectocal is licensed under the Apache 2.0 license, see [LICENSE](LICENSE) or
apache.org for details.
