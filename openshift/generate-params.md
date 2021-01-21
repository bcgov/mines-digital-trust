# Generate Parameters
This document guides you through the generating the parameter files for your templates. These files can be generated repeatedly and as often as necessary, just remember to check their values before firing any commands that use them.

**NOTE:** the *.param files checked into this repository were generated using these tools. You may not need to generate them ever again, but you should understand how to use the tool and what to do post-generation.

## Prerequisites

1. You have read through this document's parent [readme](./README.md)
1. You have installed and setup your [tooling](./tooling.md)
1. Someone has [initialized](./initialization.md) the namespaces
1. You have read through this document!

### Assumptions

1. You have cloned this repository
1. Your terminal session open and your working directory is `mines-digital-trust/openshift` (location of this file)

### Notes about examples

1. All examples will use the namespace licence plate: `a3e512`

## How-to
The *.param files in the repo are the result of generation and manual edit. However, you may find you need different values or add more parameters to your templates.  When adding more parameters, you will need to re-generate.

**Important:** The [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools) does do some internal mashing and generating, so the values in your templates may or may not end up in your *.param files as you expect or intend.

Pay particular attention to `APPLICATION_DOMAIN`. This is generated as `<component-name>-<namespace-licence-plate>-<env>-<domain-postfix>` (ex. mines-permitting-agent-a3e512-dev.apps.silver.devops.gov.bc.ca). In [settings.sh](settings.sh), we have overridden the default `APPLICATION_DOMAIN_POSTFIX` required for Openshift 4 domains. But just be aware that the value you enter for `APPLICATION_DOMAIN` in your templates will be changed on generate.

**Note:** This is one operation that did not work on Mac Mojave (did not respect `export skip_git_overrides="mines-permitting-agent-build.yaml db-build.yaml"` in `settings.sh`).

### Usage

#### Help
```sh
genParams.sh -h
```

#### Generate

The following will generated all param files (for build and deploy) for all components under `./templates`.

```sh
genParams.sh
```

The following targets a specific component (`db`)
Note the `-c` to limit to a single component.

```sh
genParams.sh -c db -f
```

The following will target a specific component (`db`)and overwrite existing .param files.
Note the `-f` for force overwrite and `-c` to limit to a single component.

```sh
genParams.sh -c db -f
```

Feel free to adjust the already generated param files if you are changing a parameter (i.e. uncommenting it for an environment or altering the value itself). Param files do nothing on their own but are used for builds (`genBuilds.sh`) and deployments (`genDepls.sh`).

#### Important notes on param generation
When we generate the parameter files, the output requires review to ensure the values are correct. Of particular note values we wish to override (ex. create passwords) using `*.overrides.sh` must be commented out.

Please review and adjust as necessary:

##### mines-permitting-agent (build)
The image we are building does not come from our repository; the parameter generator assumes we are.  Ensure that we are using the correct value for `GIT_REPO_URL` and `GIT_REF`.

`GIT_REPO_URL=https://github.com/bcgov/aries-vcr.git`
`GIT_REF=master`

##### mines-permitting-agent (deploy)

Ensure that the `APPLICATION_DOMAIN` and `AGENT_BASE_URL` have matching domains.  The Org. Book agent uses the`AGENT_BASE_URL` as the callback endpoint to facilitate communication.  Route creation uses the `APPLICATION_DOMAIN` value.

`APPLICATION_DOMAIN=mines-permitting-agent-a3e512-dev.apps.silver.devops.gov.bc.ca`
`AGENT_BASE_URL=https://mines-permitting-agent-a3e512-dev.apps.silver.devops.gov.bc.ca`


##### mines-permitting-agent-secrets (deploy)

Comment out the values we want to fill using our overrides script.

`# ADMIN_API_KEY=[a-zA-Z0-9_]{16}`
`# WALLET_KEY=[a-zA-Z0-9_]{16}`
`# AGENT_WALLET_SEED=[a-zA-Z0-9_]{16}`
`# WALLET_DID=[a-zA-Z0-9_]{16}`

**NOTE:** We have separated the secrets for the agent/wallet from the agent deployment script because we can use these values __BEFORE__ deployment. This will allow us to do registration with the Org. Book ledger before the actual deployment; reducing the number of deployments and configuration changes to start up without error.

##### mines-permitting-issuer (deploy)

Comment out the values we want to fill using our overrides script.

`# ISSUER_SECRET_KEY=[a-zA-Z0-9_]{16}`


##### mines-permitting-wallet (deploy)

Comment out the values we want to fill using our overrides script.

`# POSTGRESQL_USER=[a-zA-Z0-9]{16}`
`# POSTGRESQL_PASSWORD=[a-zA-Z0-9]{16}`
`# POSTGRESQL_ADMIN_PASSWORD=[a-zA-Z0-9]{16}`
