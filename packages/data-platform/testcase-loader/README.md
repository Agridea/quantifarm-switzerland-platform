# Testcase loader

## Running this (outside of Docker)

(assumes you are in a bash shell, such as in Linux, macOS or WSL)

- Have Python 3.11 or higher installed
- Create a virtualenv:

```bash
# You might need to change `python` into `python3` or
# `python3.11` depending on your system.
python -m venv venv
```

- Activate the virtualenv:

```bash
source ./venv/bin/activate
```

- Install the QuantiFarm common modules:

```
pip install -e ../common
```

- Install this (`testcase_loader`) module (including development dependencies):

```
pip install -e .[dev]
```

- Start the module with the correct environment variables (not needed for the general testcase data loader):

```
bash
# (assumes that the triple store is by default available at `localhost:3030`)
python -m testcase_loader
```

## Running the tests (Needs to be updated!!!)

- Follow all the steps above for installing the virtualenv and the module
- Run the tests:

```bash
python -m pytest
```

### Test tc0.json file with data

The .json file with data of an imaginary test case (`tc0.json`) is based on the schema's in folder [json-schemas](https://gitlab.com/QuantiFarm/data-platform/-/tree/main/testcase-loader/json-schemas?ref_type=heads) and is filled in with fake data.

