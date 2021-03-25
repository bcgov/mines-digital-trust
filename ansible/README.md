# Ansible for OCP4 deployments

## Setup Pre-reqs:

- Install Ansible (Used v3.1.0)
- Python

## Development

- Login with the OC cli tool to authenticate

## Registry Access

- Create service account
- Create role binding between the service account and edit registry
- Get the token from the service account's secret. Using this in a secret lets you login to the internal registry

### Update a template:

- Pull a pre-existing build / deploy config with needless metadata removed:

`cd ansible/ && python3 config_extractor.py a3e512-dev deploymentconfigs mines-permitting-issuer-primary`
