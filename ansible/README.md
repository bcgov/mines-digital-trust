# Ansible for OCP4 deployments

## Setup Pre-reqs for local dev:

- Install Ansible (Used v3.1.0)
- Python
- pip install openshift

## Development

- Login with the OC cli tool to authenticate

## How builds work

- The github runner is able to access the OCP imagestream with a service account token stored in a github secret
- The runner will build the image from the related service's directory dockerfile
- It pushes to the image stream specified in the workflow
- This image stream exists in the tools namespace
- When images are pushed to this image stream, it triggers an event which updates the related deployments

## How the infra updates work

- The github runner first uses oc to login into the silver cluster to obtain a local .kube config
- It uses this config to connect during the playbook
- The playbook is configured to run on localhost (the runner itself) and apply changes to the openshift API
- The runner itself will call the playbook. If you setup the relavant ENV variables, you can also execute it locally: `ansible-playbook apply_deployment.yaml`
- When the k8's module is invoked in the playbook, Ansible will make an idemptotent check to determine if there's any drift
- If no drift is detected, then no changes occur, so you can call the playbook as many times as you want without side effects

## Footnotes

### Registry Access

- Create service account
- Create role binding between the service account and edit registry role
- Get the token from the service account's secret. Using this in a github secret lets you login to the internal registry

### Pull a config and clean it:

NOTE: This is purely a utility script, you may not even need it

- Pull a pre-existing build / deploy config with needless metadata removed:

`cd ansible/ && python3 config_extractor.py a3e512-dev deploymentconfigs mines-permitting-issuer-primary`
