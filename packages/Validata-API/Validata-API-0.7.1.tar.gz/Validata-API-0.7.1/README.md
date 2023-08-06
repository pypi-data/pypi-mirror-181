# Validata API

[![PyPI](https://img.shields.io/pypi/v/validata-api.svg)](https://pypi.python.org/pypi/validata-api)

Web API for Validata

## Usage

You can use the online instance of Validata:

- user interface: https://go.validata.fr/
- API: https://go.validata.fr/api/v1/
- API docs: https://go.validata.fr/api/v1/apidocs

Several software services compose the Validata stack. The recommended way to run it on your computer is to use Docker. Otherwise you can install each component of this stack manually, for example if you want to contribute by developing a new feature or fixing a bug.

## Run with Docker

Read instructions at https://git.opendatafrance.net/validata/validata-docker

## Develop

### Install

We recommend using `venv` python standard package:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies (using master branch of validata-core project):

```bash
pip install -r requirements.txt
pip install -e .
```

To use a specific distant git development branch of validata_core :
```bash
pip install -r requirements.txt
pip uninstall validata_core
pip install git+https://git.opendatafrance.net/validata/validata-core.git@development-branch
pip install -e .
```


### Configure

```bash
cp .env.example .env
```

Customize the configuration variables in `.env` file.

Do not commit `.env`.

See also: https://github.com/theskumar/python-dotenv

### Serve

Start the web server...

```bash
./serve.sh
```

... then open http://localhost:5600/

### Test the API - example for schema of Infrastructures de recharge pour véhicules électriques

File to validate: https://opendata.paris.fr/explore/dataset/belib-points-de-recharge-pour-vehicules-electriques-donnees-statiques/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false

Schema used: https://schema.data.gouv.fr/schemas/etalab/schema-irve/2.1.0/schema.json

Validate data (case-sensitive validation of headers):

http://localhost:5600/validate?schema=https%3A%2F%2Fschema.data.gouv.fr%2Fschemas%2Fetalab%2Fschema-irve%2F2.1.0%2Fschema.json&url=https%3A%2F%2Fopendata.paris.fr%2Fexplore%2Fdataset%2Fbelib-points-de-recharge-pour-vehicules-electriques-donnees-statiques%2Fdownload%3Fformat%3Dcsv%26timezone%3DEurope%2FBerlin%26use_labels_for_header%3Dfalse

http://localhost:5600/validate?schema=https%3A%2F%2Fschema.data.gouv.fr%2Fschemas%2Fetalab%2Fschema-irve%2F2.1.0%2Fschema.json&url=https%3A%2F%2Fopendata.paris.fr%2Fexplore%2Fdataset%2Fbelib-points-de-recharge-pour-vehicules-electriques-donnees-statiques%2Fdownload%3Fformat%3Dcsv%26timezone%3DEurope%2FBerlin%26use_labels_for_header%3Dfalse&header_case=True



Validate data (case-insensitive validation of headers):

http://localhost:5600/validate?schema=https%3A%2F%2Fschema.data.gouv.fr%2Fschemas%2Fetalab%2Fschema-irve%2F2.1.0%2Fschema.json&url=https%3A%2F%2Fopendata.paris.fr%2Fexplore%2Fdataset%2Fbelib-points-de-recharge-pour-vehicules-electriques-donnees-statiques%2Fdownload%3Fformat%3Dcsv%26timezone%3DEurope%2FBerlin%26use_labels_for_header%3Dfalse&header_case=False

## Release a new version

- Update version in [setup.py](setup.py) and [CHANGELOG.md](CHANGELOG.md) files
- Commit changes using `Release` as commit message
- Create git tag (starting with "v" for the release)
- Git push: `git push && git push --tagss`
- Check that container image is well built and pypi package is created ([validata-api pipelines](https://git.opendatafrance.net/validata/validata-api/-/pipelines))
