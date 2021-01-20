# Initialization
This document guides you through the initialization phase. The four namespaces require a little setup before we can continue with deploying our code.

## Prerequisites

1. You have read through this document's parent [readme](./README.md)
1. You have installed and setup your [tooling](./tooling.md)
1. You have read through this document!

### Assumptions

1. You have administrator permissions to your four project namespaces (*-dev, *-test, *-prod, *-tools)
1. You have cloned this repository
1. Your terminal session is logged into Openshift and your working directory is `mines-digital-trust/openshift` (location of this file)

### Notes about examples

1. All examples will use the namespace licence plate: `a3e512`

## Initialize Namespaces
The four project namespaces need to have special service account permissions to allow image building and pulling.

```sh
initOSProjects.sh
```

## Set Network Security Policies
The following is not the ideal setup of network security policies; please keep in mind that we will update our NSPs later.

```sh
oc -n a3e512-tools process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=tools | oc -n a3e512-tools create -f -
oc -n a3e512-dev process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=dev | oc -n a3e512-dev create -f -
oc -n a3e512-test process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=test | oc -n a3e512-test create -f -
oc -n a3e512-prod process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=prod | oc -n a3e512-prod create -f -
```
