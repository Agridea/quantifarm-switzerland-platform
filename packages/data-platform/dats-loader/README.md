# DATs loader

## Running this (outside of Docker)

(assumes you are in a bash shell, such as in Linux, macOS or WSL)

- Have Python 3.11 installed
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

- Install this (`dats_loader`) module:

```
pip install -e .
```

- Have `fairshare-dats-06-2024.json` in this directory (get it from our Google Drive folder).
- Start the module:

```bash
# (assumes that the triple store is available at `localhost:3030`)
python -m dats_loader
```
