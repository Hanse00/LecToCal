from setuptools import setup, find_packages
from codecs import open

def readme():
    with open("README.rst", encoding="utf-8") as f:
        return f.read()

setup(
    name="lectocal",
    version="1.0.0a5",
    description="Syncronize Lectio schedules to Google Calendar.",
    long_description=readme(),
    url="https://github.com/Hanse00/LecToCal",
    author="Philip Mallegol-Hansen",
    author_email="philip@mallegolhansen.com",
    license="Apache 2.0",
    python_requires=">=3",
    classifiers=[
        # Development Status
        "Development Status :: 3 - Alpha",

        # Audience / Topic
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Education",
        "Topic :: Utilities",

        # Supported Versions
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",

        # Environment Type
        "Environment :: No Input/Output (Daemon)",
        "Environment :: Web Environment",

        # License
        "License :: OSI Approved :: Apache Software License"
    ],
    keywords="lectio google calendar sync utility",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "requests",
        "lxml",
        "pytz",
        "python-dateutil"
    ],
    package_data={
        "lectocal": [
            "client_secret.json",
        ]
    },
    entry_points={
        "console_scripts": [
            "lectocal.run=lectocal.run:main",
            "lectocal.gauth=lectocal.gauth:main"
        ]
    }
)
