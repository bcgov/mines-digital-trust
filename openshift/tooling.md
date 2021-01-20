# Tooling
This document guides you through the tooling and scripts required to intialize the namespaces and deploy the code. This is proprietary (but open source) tooling which will (should) help with some pretty complex procedures.

## Prerequisites

1. You have read through this document's parent [readme](./README.md)
1. You have read through this document!

### Assumptions

1. You have administrator permissions to your four project namespaces (*-dev, *-test, *-prod, *-tools)

## Installation
1. Clone this repository, navigate to your `mines-digital-trust/openshift` directory
1. install [openshift command-line interface](https://docs.openshift.com/container-platform/4.6/cli_reference/openshift_cli/getting-started-cli.html) for your Operating System
1. install [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools), configure for your particular Operating System (or see [Alternative Tools](#alternative-tools))
1. ensure you have [curl](https://curl.se) or some other method to run http(s) requests installed

### Alternative Tools
Use the [Dockerfile](./Dockerfile) to run the openshift developer tools.  You will need Docker (obviously), and you will need to build the image and mount your local cloned repository code. The Dockerfile may be a better alternative with Mac, some commands in the scripts do not work as expected (ex. `echo -n` and `export -a`).  This docker image does contain [curl](https://curl.se) so examples will work.

This document assumes you are in a terminal at your cloned mines-digital-trust/openshift directory. The following will mount this directory at `/usr/src/app/openshift` and log you in there.

```sh
docker build --tag os-dev-tools:1.0 .
export w_dir=/usr/src/app/openshift
docker run -it --rm --name odt -v $(pwd):$w_dir -w $w_dir os-dev-tools:1.0

bash-5.0# <run your oc login and openshift developer tool scripts>
bash-5.0# exit
```

## Login

1. open your terminal to this folder (`mines-digital-trust/openshift`)
1. login to [openshift web console](https://console.apps.silver.devops.gov.bc.ca/k8s/cluster/projects/a3e512-tools), get your login token
1. paste your login command to your terminal
1. you are now ready to run `oc`
