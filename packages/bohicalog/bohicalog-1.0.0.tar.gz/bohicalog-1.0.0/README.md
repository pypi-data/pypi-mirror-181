<!--
<p align="center">
  <img src="https://github.com/BOHICA-Labs/bohicalog/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  BOHICA Logging Library
</h1>

<p align="center">
    <a href="https://github.com/BOHICA-Labs/bohicalog/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/BOHICA-Labs/bohicalog/workflows/Tests/badge.svg" />
    </a>
    <a href="https://pypi.org/project/bohicalog">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/bohicalog" />
    </a>
    <a href="https://pypi.org/project/bohicalog">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/bohicalog" />
    </a>
    <a href="https://github.com/BOHICA-Labs/bohicalog/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/bohicalog" />
    </a>
    <a href='https://bohicalog.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/bohicalog/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://codecov.io/gh/BOHICA-Labs/bohicalog/branch/main">
        <img src="https://codecov.io/gh/BOHICA-Labs/bohicalog/branch/main/graph/badge.svg" alt="Codecov status" />
    </a>  
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-snekpack-blue" /> 
    </a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' />
    </a>
    <a href="https://github.com/BOHICA-Labs/bohicalog/blob/main/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Contributor Covenant"/>
    </a>
</p>

The BOHICA Logging Library provides a configured logger for you module or application

## 💪 Getting Started

Example Usage
-------------

```python
from bohicalog import logger

logger.debug("hello")
logger.info("info")
logger.warning("warn")
logger.error("error")

# This is how you'd log an exception
try:
    raise Exception("this is a demo exception")
except Exception as e:
    logger.exception(e)

# JSON logging
import bohicalog
bohicalog.json()

logger.info("JSON test")

# Start writing into a logfile
bohicalog.logfile("/tmp/bohicalog-demo.log")

# Set a minimum loglevel
bohicalog.loglevel(bohicalog.WARNING)
```

This is the output:

![demo-output](https://raw.githubusercontent.com/bohica-labs/bohicalog/master/docs/_static/demo-output-json.png)

Note: You can find more examples in the documentation: https://bohicalog.readthedocs.io

### JSON logging

JSON logging can be enabled for the default logger with `bohicalog.json()`, or with `setup_logger(json=True)` for custom loggers:

```python
>>> bohicalog.json()
>>> logger.info("test")
{"asctime": "2022-12-21 10:42:45,808", "filename": "<stdin>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 1, "module": "<stdin>", "message": "test", "name": "bohicalog_default", "pathname": "<stdin>", "process": 76179, "processName": "MainProcess", "threadName": "MainThread"}

>>> my_logger = setup_logger(json=True)
>>> my_logger.info("test")
{"asctime": "2022-12-21 10:42:45,808", "filename": "<stdin>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 1, "module": "<stdin>", "message": "test", "name": "bohicalog_default", "pathname": "<stdin>", "process": 76179, "processName": "MainProcess", "threadName": "MainThread"}
```

The logged JSON object has these fields:

```json
{
  "asctime": "2022-12-21 10:43:40,765",
  "filename": "test.py",
  "funcName": "test_this",
  "levelname": "INFO",
  "levelno": 20,
  "lineno": 9,
  "module": "test",
  "message": "info",
  "name": "bohicalog",
  "pathname": "_tests/test.py",
  "process": 76204,
  "processName": "MainProcess",
  "threadName": "MainThread"
}
```

Exceptions logged with `logger.exception(e)` have these additional JSON fields:

```json
{
  "levelname": "ERROR",
  "levelno": 40,
  "message": "this is a demo exception",
  "exc_info": "Traceback (most recent call last):\n  File \"_tests/test.py\", line 15, in test_this\n    raise Exception(\"this is a demo exception\")\nException: this is a demo exception"
}
```

Take a look at the documentation for more information and examples:

* Documentation: https://bohicalog.readthedocs.io.



## 🚀 Installation

<!-- Uncomment this section after your first ``tox -e finish``
The most recent release can be installed from
[PyPI](https://pypi.org/project/bohicalog/) with:

```bash
$ pip install bohicalog
```
-->

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/BOHICA-Labs/bohicalog.git
```

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.md](https://github.com/BOHICA-Labs/bohicalog/blob/master/.github/CONTRIBUTING.md) for more information on getting involved.

## 👋 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Harvard Program in Therapeutic Science - Laboratory of Systems Pharmacology](https://hits.harvard.edu/the-program/laboratory-of-systems-pharmacology/)

-->

<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body                                             | Program                                                                                                                       | Grant           |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------|
| DARPA                                                    | [Automating Scientific Knowledge Extraction (ASKE)](https://www.darpa.mil/program/automating-scientific-knowledge-extraction) | HR00111990009   |
-->

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.

## 🛠️ For Developers

<details>
  <summary>See developer instructions</summary>


The final section of the README is for if you want to get involved by making a code contribution.

### Development Installation

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/BOHICA-Labs/bohicalog.git
$ cd bohicalog
$ pip install -e .
```

### 🥼 Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/BOHICA-Labs/bohicalog/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```shell
$ git clone git+https://github.com/BOHICA-Labs/bohicalog.git
$ cd bohicalog
$ tox -e docs
$ open docs/build/html/index.html
``` 

The documentation automatically installs the package as well as the `docs`
extra specified in the [`setup.cfg`](setup.cfg). `sphinx` plugins
like `texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses [Bump2Version](https://github.com/c4urself/bump2version) to switch the version number in the `setup.cfg`,
   `src/bohicalog/version.py`, and [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using [`build`](https://github.com/pypa/build)
3. Uploads to PyPI using [`twine`](https://github.com/pypa/twine). Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion minor` after.
</details>
