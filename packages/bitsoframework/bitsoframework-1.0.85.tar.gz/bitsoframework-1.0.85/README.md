# Bitso Framework

Python library companion for the Bitso Framework

## How to build from source

```bash
git clone ...
cd bitsoframework
python3 -m venv .python-env
source .python-env/bin/activate
pip install -r base.txt

#
# at least once to set up all your libraries needed to build
#
source scripts/pre-build.sh

#
# actually build the local package
#
source scripts/build.sh

```

## PYPI

To set credentials to publish you may run the following command:

python3 -m keyring set https://upload.pypi.org/legacy/ bitso

Docker Quick Start
-----------
This project creates a shared database.
If using docker it will create a shared network and volume that the other projects can connect to.

Start bitsoframework by running `docker-compose -f local.yml up --build`

If you are missing the network or volume you will see the following prompts:
  - create network with `docker network create bitso_local_network`
  - create volume with `docker volume create --name=bitso_local_db_volume`