# LecToCal

LecToCal is a python module for syncronizing Lectio schedules into Google Calendar.

By writing the schedule into Calendar in the native format, it supports notifications, viewing from Android and iOS, and everything else normally possible with a Google Calendar.

## Installation

Installation is easiest using pip, as LecToCal is availble on Pypi as a package (http://pypi.org/project/lectocal/). Simply run `pip install lectocal`.

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

    After the OAuth credential exists, LecToCal can now write into the calendar using the API.

    Running `lectocal.run` at this point, scrapes the schedule for the chosen individual, and writes it to the calendar.

1. Repeat.

    To keep a calendar up to date, step 2 will need to be repeated at a given interval.
    This can for example be done using cron, or a similar task scheduling system.

    As long as the OAuth credentials are not deleted from the system, or revoked from the Google account, step 1 should not need to be re-run.

**Note**

The generated Google Calendar should not be deleted or renamed, this may cause the system to break, or act in unexpected ways, such as creating a duplicate calendar.

## Development

We love Pull Requests!

If you're interested in the project, and have an idea for something that can be improved, please feel welcome to contribute.

If you're not sure if your idea would be approved, open an issue on GitHub, or use the mailing list first.

Once you have the source, we strongly recommend using Pipenv.

Pipenv makes it easy to install the correct dependencies, so you can start working with the code.

Once you have pipenv installed on your system, navigate to the directory where this project is stored, then run:
`pipenv install --dev`

This will create a pipenv with the right python version (If installed on your system) and all required dependencies.

At which point `pipenv shell` will put you in a shell where all those are available.

Happy coding!

## Bugs, Feedback, Thoughts, etc.

For bugs or pull requests, please use the builtin GitHub issue tracker.

For everything else use lectocal@googlegroups.com.

## Donations

If you'd like to buy me a coffee - Awesome!
If you're not in a position to do that, please enjoy the software just the same - It's free for a reason.

Currently I accept BTC at: 3P4bzcKTvkz4Ey3QrAdiPa1zBKWVwsVqMb

## License

LecToCal is licensed under the Apache 2.0 license, see [LICENSE](LICENSE) or
apache.org for details.