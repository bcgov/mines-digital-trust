# Ongoing Deployments
This document guides you through ongoing deployments. These could be configuration changes (ex. change logging level), code changes (ex. updates to your issuer schema), bug fixes, or adding new components into your overall application.

## Prerequisites

1. You have read through this document's parent [readme](./README.md)
1. You have installed and setup your [tooling](./tooling.md)
1. Someone has [initialized](./initialization.md) the namespaces
1. Someone has [generated](./generated-params.md) deployment parameter files
1. Someone has done the initial [first deployments](./first-deployments.md)
1. You have read through this document!

### Assumptions

1. You have administrator permissions to your four project namespaces (*-dev, *-test, *-prod, *-tools)
1. Your terminal session is logged into Openshift and your working directory is `mines-digital-trust/openshift` (location of this file)

### Notes about examples

1. All http(s) requst examples will be in [curl](https://curl.se)
1. All examples will use the namespace licence plate: `a3e512`
1. All examples will use the `dev` environment (`a3e512-dev`), replace `dev` and `a3e512-dev` when appropriate
1. All examples will use the `mines-permitting-issuer` component

## Basic Ongoing Scenario
The most common use case is deploying changes to an issuer.

We start by deploying to `dev`, if changes are tested and accepted, we promote to `test`, then `prod` environments.

### deploy to dev
1. update build config
1. build image
1. tag image
1. update deployment config
1. deploy
1. do quality assurance and testing


#### update build config
Assuming that we have changed the source code for our issuer (or added components to our [build configuration](./templates/mines-permitting-issuer/mines-permitting-issuer-build.json)), we must update our image.  This is how we do it.

**Important:** the `-u` flag to indicate update, not create.

```sh
genBuilds.sh -c mines-permitting-issuer -u
```

#### build image
The `genBuilds` should start a build, if it does not, you can manually trigger a build from the command line like so:

```sh
oc -n a3e512-tools start-build mines-permitting-issuer --follow
```

#### tag image
After a build, we need to tag the image for use in `dev`.  Same as in [firt deployment](./first-deployments.md).

```sh
oc -n a3e512-tools tag mines-permitting-issuer:latest mines-permitting-issuer:dev
```

#### update deployment config
If we have made changes to our [deployment configuration](./templates/mines-permitting-issuer/mines-permitting-issuer-deploy.json) (ex. add environment variables), or we simply want to deploy our updated image, we do the following:

**Important:** the `-u` flag to indicate update, not create.

```sh
genDepls.sh -c mines-permitting-issuer -e dev -u
```

#### deploy
The `genDepls` should re-deploy pods with our updated image (and configuration), if it does not, you can manually trigger a deployment from the command line like so:

**Note:** because we updated the [deployment configuration](./templates/mines-permitting-issuer/mines-permitting-issuer-deploy.json) in `dev`, we rollout in `a3e512-dev`, not `a3e512-tools`.

```sh
oc -n a3e512-dev rollout latest dc/mines-permitting-issuer-primary
```

#### do quality assurance and testing
Run any test scripts or procedures deemed necessary to prove the changes are effective and works as expected. If all is good, we promote to `test`.

### promotion to test
Promotion is a little simpler as the updated image is already built. We want the image (and configuration changes) in `dev` pushed to `test`.  Here's how we do it:

1. tag image
1. update deployment config
1. deploy
1. do quality assurance and testing

#### tag image
The image has been built, and it has been verified for quality in `dev`; we simply want to move that updated image into `test`. We do **NOT** tag the `latest` image from `tools`, we tag the `dev` image itself (which may or may not be `latest`).

```sh
oc -n a3e512-tools tag mines-permitting-issuer:dev mines-permitting-issuer:test
```

#### update deployment config
We need to follow the same procedure as in `dev`.

```sh
genDepls.sh -c mines-permitting-issuer -e test -u
```

#### deploy
The `genDepls` should re-deploy pods with our updated image (and configuration), if it does not, you can manually trigger a deployment from the command line like so:

**Note:** because we updated the [deployment configuration](./templates/mines-permitting-issuer/mines-permitting-issuer-deploy.json) in `test`, we rollout in `a3e512-test`, not `a3e512-tools`.

```sh
oc -n a3e512-test rollout latest dc/mines-permitting-issuer-primary
```

#### do quality assurance and testing
Run any test scripts or procedures deemed necessary to prove the changes are effective and works as expected. If all is good, we promote to `prod`.

### promotion to prod
Promotion to `prod` is the same as `test`.  However, we are affecting access to our services; schedule, plan, and notify clients appropriately.

1. tag image
1. update deployment config
1. deploy
1. do quality assurance and testing

#### tag image


```sh
oc -n a3e512-tools tag mines-permitting-issuer:test mines-permitting-issuer:prod
```

#### update deployment config
We need to follow the same procedure as in `test`.

```sh
genDepls.sh -c mines-permitting-issuer -e prod -u
```

#### deploy
The `genDepls` should re-deploy pods with our updated image (and configuration), if it does not, you can manually trigger a deployment from the command line like so:

```sh
oc -n a3e512-prod rollout latest dc/mines-permitting-issuer-primary
```

#### do quality assurance and testing
Run any test scripts or procedures deemed necessary to prove the changes are effective and works as expected. Notify anyone that needs to know new code is live in production.

## Updating a secret
If you need to add a key/value pair to an existing secret, the simplest way is to do it in your Openshift web console.

Either you have been given a value to use for you secret (ex. an API Key to external system), or you will need to generate a new value.

### Generating values
If you require to generate a value, first, determine what you need generating (key, seed, password, username), then use one of the utility files to generated it. These scripts are wrappers around the developer tool functions used elsewhere to generate values for our secrets.

1. grant execute permissions to the [utils](./utils) files
1. run a script
1. save the value

```sh
chmod -R u+x ./utils/*.sh

# generate a key (default is length of 48, pass in a different length if you want)
./utils/generateKey.sh 32

Initializing generateKey ...
Generate Key (length=32)
zG/Y/tf7GAP7gVea4DMUts6C+BRLdb+mJHeLw4E+pt4=

# generate a seed (prefix is '', pass in a different one if required)
./utils/generateSeed.sh

Initializing generateSeed ...
Generate Seed (prefix = )
xJ5nCw0+Fgad5imoB1+MthebP9rvC0Jm

# generate a password
./utils/generatePassword.sh

Initializing generatePassword ...
Generate Password
MBcXGIbgtKi57Rye2R3s

# generate a username
./utils/generateUsername.sh

Initializing generateUsername ...
Generate Username
User_1GBKr0Qj

```

### Updating/Adding key/value
1. login to Openshift
1. navigate to your Secret, select Actions / Edit Secret
1. add your new key value pair
1. save your updated secret

Then you would follow your procedures for deployment, as this would assume you have added the new value as an environment variable for you container/image/code.
