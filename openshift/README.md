
# Manual Build and Deploy

## Prerequisites
1. you will need administrator permissions to your 4 project namespaces (*-dev, *-test, *-prod, *-tools)
1. install [openshift command-line interface](https://docs.openshift.com/container-platform/4.6/cli_reference/openshift_cli/getting-started-cli.html) for your Operating System
1. install [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools), configure for your particular Operating System
1. clone this repo

### Alternative
Use the [Dockerfile](./Dockerfile) to run the openshift developer tools.  You will need Docker (obviously) and you will need to build the image, and mount your local cloned repository code. This may be a better alternative with Mac, some commands in the scripts do not work as expected (ex. `echo -n` and `export -a`)

This assumes you are in a terminal/console at your cloned mines-digital-trust/openshift directory.

```sh
docker build --tag os-dev-tools:1.0 .
docker run -it --rm --name odt -v /<yourpathto>/mines-digital-trust/openshift:/usr/src/app/openshift os-dev-tools:1.0

bash-5.0# cd /usr/src/app/openshift
bash-5.0# <run your oc login and openshift developer tool scripts>
bash-5.0# exit
```

## Assumptions
This assumes you have the 4 namespaces and they are clean. This guide is to set up from scratch.

The following will always assume you are in your terminal/console, logged in to `oc` and at `mines-digital-trust/openshift` directory. Note that this is the initial install and setup for the project, assumes all empty project namespaces and we are only setting up `dev`.

Namespaces as defaults in *-deploy.yamls and the following commands are for *__a3e512__*, change as necessary.

For this guide, we are only setting up the `dev` namespace.

### Issues
The templates that these were based on did not work out of the box, so some adjustments were made and should be addressed in the future.  For instance, in this guide we will install very wide-open network security policies.  These should be refined to expose only the bare minimum access necessary.

## Project Namespace setup
1. open terminal/console to this folder (mines-digital-trust/openshift)
1. login to openshift web console, get your login token
1. paste your login command to your terminal/console
1. initialize the namespaces

```sh
initOSProjects.sh
```

### Add network security policies
As mentioned above, this is not the ideal setup of network security policies, please keep in mind that we will update our NSPs at a later time.

```sh
oc -n a3e512-tools process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=tools | oc -n a3e512-tools create -f -
oc -n a3e512-dev process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=dev | oc -n a3e512-tools create -f -
```

### Generate openshift-developer-tools params files
The *.param files in the repo have already been generated. However, you may find you need different values, or need to add more parameters to your templates.  When adding more parameters, you will need to re-generate. This is one operation that did not work on Mac Mojave (did not respect `export skip_git_overrides="agent-build.yaml db-build.yaml"` in `settings.sh`).

1. Review the generate params options

```sh
genParams.sh -h
```

Note the `-f` for force overwrite and `-c` to limit to a single component.

Example: force overwrite the db params.

```sh
genParams.sh -c db -f
```

Feel free to adjust the already generated param files if you are changing a parameter (i.e. uncommenting it for an environment or altering the value itself). Param files do nothing on their own, but are used for builds (`genBuilds.sh`) and deployments (`genDepls.sh`).

### Wallet
#### base db image
######IMPORTANT
ensure the `db-build.param` contains:

```
GIT_REPO_URL=https://github.com/WadeBarnes/von-bc-registries-agent-configurations.git
GIT_REF=feature/ocp4
```

1. generate the database image stream (builds/image streams are in the tools namespace)
1. wait until image stream is built
1. tag for use in *-dev namespace


```sh
genBuilds.sh -c db
oc -n a3e512-tools tag db:latest db:dev
```

#### deploy wallet db
######IMPORTANT
We have an wallet-deploy.overrides.sh that will generate usernames, passwords and seeds for us. In order for it to work, we need to comment out the values for `POSTGRESQL_USER`, `POSTGRESQL_PASSWORD`, `POSTGRESQL_ADMIN_PASSWORD` in `wallet-deploy.param`.  Make sure those are commented out.

1. run the deployment for wallet db (deployments are in the dev namespace)

```sh
genDepls.sh -e dev -c wallet
```

If you encounter issues, check that the `wallet-primary` secret contains the generated values, such as `database-user = User_zmQn2wc2`.

### Agent

#### base agent (aries-vcr) image
######IMPORTANT
ensure the `agent-build.param` contains:

```
GIT_REPO_URL=https://github.com/bcgov/aries-vcr.git
GIT_REF=master
```

1. generate the agent image stream
1. wait until image stream is built
1. tag for use in *-dev namespace

```sh
genBuilds.sh -c agent
oc -n a3e512-tools tag agent:latest agent:dev
```

#### deploy agent
######IMPORTANT
We have an agent-deploy.overrides.sh that will generate usernames, passwords and seeds for us. In order for it to work, we need to comment out the values for `ADMIN_API_KEY`, `WALLET_KEY`, `AGENT_WALLET_SEED` and `WALLET_DID` in `agent-deploy.param`.  Make sure those are commented out.

The initial deployment will prompt you for input, just hit <enter> and accept the defaults for this first initial run through.

```sh
genDepls.sh -e dev -c agent
```

This will deploy with 0 replicas, the agent will not spin up, but we need to grab the generated values from the secret to register our agent with the ledger.

#### authenticate/register agent with ledger

1. Go to http://dev.bcovrin.vonx.io
2. see the Authenicate a New DID panel, select Register from Seed.
3. Copy value for seed from `agent-wallet-credentials-primary` secret
4. set Wallet Seed = secret value
5. set Alias = emli-permit-agent
6. click Register DID

#### stand up agent

1. Edit `agent-deploy.yaml` line 102, change `replicas: 0` to `replicas: 1` for the DeploymentConfig.
2. Update the deployment, which will spin up the pods and create an encrypted wallet.

```sh
genDepls.sh -e dev -c agent -u
```

Note that the `-u` will respect the changes in param files and in the `agent-deploy.yaml` itself; in this update it will set the replica count to 1 which will deploy pods.  It will *not* overwrite or change the secrets - this is very important.

#### verify agent
We can verify the agent by hitting its admin port. We do not want to create a public route to the admin port, so we can use port-forwarding to connect through our local machine.

The following is an example on Mac, you may need to adjust to your particular machine.

```sh
# get a pod name
oc -n a3e512-dev get pods -o name --selector role=agent,name=agent-primary
> pod/agent-primary-1-6wvnq
> pod/agent-primary-1-tzjp6

# port forward and store the process id
oc -n a3e512-dev port-forward pod/agent-primary-1-6wvnq 28024:8024 > /dev/null 2>&1 & AGENT_ADMIN_PORT_FORWARD_PID=$!

# run any connections/tests through POSTMAN or curl

# kill the process when you are done
kill -9 $AGENT_ADMIN_PORT_FORWARD_PID
```

1. From the `agent-primary` secret, copy the value for `admin-api-key`
2. check the agent connections

```sh
curl --location --request GET 'http://localhost:28024/connections' \
--header 'X-API-KEY: <your agent-primary admin-api-key value>'

# expect 200 OK with {results: []} , there are no connections yet...
```

#### invitations to Org Book
This section is a work in progress. There was an issue getting this to work in the ideal way, so we fudged it. Update this section when the issue is sorted out.

1. Send a request to the VON Team [rocketchat #von-general](https://chat.pathfinder.gov.bc.ca/channel/von-general) for an inivitation to Org Book DEV.
2. Copy the JSON they provide
3. In POSTMAN (or curl or other), POST the invitation with an alias to the Org Book agent (`icob-agent` - see the value for label in the invitation), remember to use your Admin API Key header. `/connections/receive-invitation?alias=icob-agent`
4. Using the returned value, find the `connection-id`.  POST that to `/connections/<connid>/accept-invitation`.
5. Check your connection to `icob-agent` is active.  GET `/connections/<connid>`

Example:

```
curl --location --request POST 'http://localhost:28034/connections/receive-invitation?alias=icob-agent' \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <your agent-primary admin-api-key value>' \
--data-raw '{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "@id": "f4ec7445-7603-4a92-9d92-0d344c7fc136",
    "label": "icob-agent",
    "recipientKeys": [
      "1Ydw7CzbvoLFf8FYDCRxqh6rtwBrxEWesqSi1ULtQnJk"
    ],
    "serviceEndpoint": "https://agent-dev.orgbook.gov.bc.ca"
  }'

curl --location --request POST 'http://localhost:28034/connections/<connid>/accept-invitation' \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <your agent-primary admin-api-key value>'

curl --location --request GET 'http://localhost:28034/connections/<connid>' \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <your agent-primary admin-api-key value>'
```

What this should do is connect to Org Book and then resolve as an active connection in your connections (`curl --location --request POST 'http://localhost:28034/connections`). However, this did not work for us as of today.  So we sent an invitation to Org Book for them to accept and that set up an active connection on both sides.

Example:

```
curl --location --request POST 'http://localhost:28024/connections/create-invitation?alias=icob-agent' \
--header 'X-API-KEY: <your agent-primary admin-api-key value>' \
--header 'Content-Type: application/json'
```

### Issuer/Controller

#### issuer controller image
######IMPORTANT
ensure the `issuer-controller-build.param` contains the correct branch for your code:

```
GIT_REPO_URL=https://github.com/bcgov/mines-digital-trust.git
GIT_REF=init-openshift
```
We are currently building the image from a branch (`init-openshift`).


1. generate the issuer controller image stream
1. wait until image stream is built
1. tag for use in *-dev namespace

```sh
genBuilds.sh -c issuer-controller
oc -n a3e512-tools tag issuer-controller:latest issuer-controller:dev
```

#### deploy issuer controller
######IMPORTANT
We have an agent-deploy.overrides.sh that will generate usernames, passwords and seeds for us. In order for it to work, we need to comment out the values for `CR_AGENT_ADMIN_URL`, `CR_ADMIN_API_KEY`, `CR_CONNECTION_NAME`, `CR_API_URL` and `CR_APP_URL` in `issuer-controller-deploy.param`.  Make sure those are commented out.

The initial deployment will prompt you for input, just hit <enter> and accept the defaults for this first initial run through.

```sh
genDepls.sh -e dev -c issuer-controller
```

This will deploy with with a route to our issuer-controller (https://issuer-a3e512-dev.apps.silver.devops.gov.bc.ca). In the future, we will have an application and user interface and not require this route; this is only in place to demonstrate issuing credentials (we could use port forwarding to achieve this too).

Ok... now that we have an issuer/controller, we can redeploy our agent with a webhook!

#### stand up agent

1. Edit `agent-deploy.param`, uncomment `WEBHOOK_URL`.
2. Update the deployment, which will spin up the pods with a populate webhook that facilitates our agent calling back to our issuer.

```sh
genDepls.sh -e dev -c agent -u
```

### Issue Credential
Using our temporary public route, issue a credential.

1. POST credentials to our issuer at `issue-credential'
2. Go [Dev Org Book](https://dev.orgbook.gov.bc.ca/en/home) and search for your entity (`Youra Permit`)

```
curl --location --request POST 'https://issuer-a3e512-dev.apps.silver.devops.gov.bc.ca/issue-credential' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "schema": "my-registration.empr",
        "version": "1.0.0",
        "attributes": {
            "corp_num": "ABC12345",
            "registration_date": "2018-01-01",
            "entity_name": "Youra Permit",
            "entity_name_effective": "2018-01-01",
            "entity_status": "ACT",
            "entity_status_effective": "2019-01-01",
            "entity_type": "ABC",
            "registered_jurisdiction": "BC",
            "addressee": "A Person",
            "address_line_1": "123 Some Street",
            "city": "Victoria",
            "country": "Canada",
            "postal_code": "V1V1V1",
            "province": "BC",
            "effective_date": "2019-01-01",
            "expiry_date": ""
        }
    },
    {
        "schema": "bcgov-mines-act-permit.empr",
        "version": "1.0.0",
        "attributes": {
            "permit_id": "MYPERMIT12345",
            "entity_name": "Youra Permit",
            "corp_num": "ABC12345",
            "permit_issued_date": "2018-01-01",
            "permit_type": "ABC",
            "permit_status": "OK",
            "effective_date": "2019-01-01"
        }
    }
]'
```


## Clean up
The following are some commands to help you remove resources from Openshift.

```sh
oc -n a3e512-dev delete all,pods,services,secrets,routes,dc,pvc,hpa,nsp -l="name=wallet-primary"

oc -n a3e512-dev delete all,pods,services,secrets,routes,dc,pvc,hpa,nsp -l="name=agent-primary"

oc -n a3e512-dev delete all,pods,services,secrets,routes,dc,pvc,hpa,nsp -l="name=issuer-controller-primary"
```

```sh
oc -n a3e512-tools delete bc,build,is,imagestreamtag -l="name=db"

oc -n a3e512-tools delete bc,build,is,imagestreamtag -l="name=agent"

oc -n a3e512-tools delete bc,build,is,imagestreamtag -l="name=issuer-controller"
```
