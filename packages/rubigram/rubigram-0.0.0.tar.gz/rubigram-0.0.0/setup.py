from setuptools import (find_packages, setup)


setup(
    name = "rubigram",

    version = "0.0.0",

    description = "an asynchronous library in Python 3 for creating bots in rubika.",

    license = "GPLv3",

    author = "albu",

    author_email = "albuorg@gmail.com",

    url = "https://github.com/ALBU-ORG/rubigram",

    packages = find_packages(exclude=["rubigram*"]),

    python_requires = ">=3.7",
)