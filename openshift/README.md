# Manual Build and Deploy

## Prerequisites
1. you will need administrator permissions to your 4 project namespaces (*-dev, *-test, *-prod, *-tools)
1. install [openshift command-line interface](https://docs.openshift.com/container-platform/4.6/cli_reference/openshift_cli/getting-started-cli.html) for your Operating System
1. install [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools), configure for your particular Operating System
1. clone this repo

## Project Namespace setup
1. open terminal/console to this folder (mines-digital-trust/openshift)
1. login to openshift web console, get your login token
1. paste your login command to your terminal/console
1. initialize the namespaces

```sh
initOSProjects.sh
```

The following will always assume you are in your terminal/console, logged in to oc and at mines-digital-trust/openshift directory. Note that this is the initial install and setup for the project, assumes all empty project namespaces.

Namespaces as defaults in *-deploy.yamls and the following commands are for *_a3e512_*, change as necessary.

### Wallet DB

#### base db image
1. generate the database image stream
1. wait until image stream is built
1. tag for use in *-dev namespace

```sh
genBuilds.sh -c db
oc -n a3e512-tools tag db:latest db:dev
```

#### deploy wallet db
```sh
genDepls.sh -e dev -c wallet
```

### Agent

#### base agent (aries-vcr) image
1. generate the agent image stream
1. wait until image stream is built
1. tag for use in *-dev namespace

```sh
genBuilds.sh -c db
oc -n a3e512-tools tag agent:latest agent:dev
```

#### deploy wallet db
The initial deployment will prompt you for input, just hit <enter> and accept the defaults for this first initial run through.

```sh
genDepls.sh -e dev -c agent
```

## Tear down
The following commands will remove components from the dev namespace assuming all defaults were used.

```sh
oc -n a3e512-dev delete pods,services,secrets,routes,dc,pvc,horizontalpodautoscaler.autoscaling,ExternalNetwork,NetworkSecurityPolicy -l="name=agent-primary"
oc -n a3e512-dev delete nsp -l="name=pods-to-k8s-api-primary"
oc -n a3e512-dev delete all,secrets,pvc -l="name=wallet-primary"
```
