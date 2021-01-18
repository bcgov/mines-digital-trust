# Configure, Build, Deploy

[toc]

### Prerequisites
1. you will need administrator permissions to your four project namespaces (*-dev, *-test, *-prod, *-tools)
1. install [openshift command-line interface](https://docs.openshift.com/container-platform/4.6/cli_reference/openshift_cli/getting-started-cli.html) for your Operating System
1. install [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools), configure for your particular Operating System (or see [Alternative Tools](#alternative-tools))
1. clone this repo

#### Alternative Tools
Use the [Dockerfile](./Dockerfile) to run the openshift developer tools.  You will need Docker (obviously), and you will need to build the image and mount your local cloned repository code. The Dockerfile may be a better alternative with Mac, some commands in the scripts do not work as expected (ex. `echo -n` and `export -a`)

This document assumes you are in a terminal at your cloned mines-digital-trust/openshift directory. The following will mount this directory at `/usr/src/app/openshift` and log you in there.

```sh
docker build --tag os-dev-tools:1.0 .
export w_dir=/usr/src/app/openshift
docker run -it --rm --name odt -v $(pwd):$w_dir -w $w_dir os-dev-tools:1.0

bash-5.0# <run your oc login and openshift developer tool scripts>
bash-5.0# exit
```

### Assumptions
The following will always assume you are in your terminal, logged in to `oc` and at `mines-digital-trust/openshift` directory (this file's location).

Namespaces as defaults in *-deploy.yaml files and the following commands are for *__a3e512__*, change as necessary.

We will use the `dev` environment and namespace for the following examples.

1. open your terminal to this folder (mines-digital-trust/openshift)
1. login to openshift web console, get your login token
1. paste your login command to your terminal
1. run your commands

### Preliminary Housekeeping Tasks
These tasks are complete; they are documented here for reference purposes.

#### Initialize Namespaces
The four project namespaces need to have special service account permissions to allow image building and pulling.

```sh
initOSProjects.sh
```

#### Set Network Security Policies
The following is not the ideal setup of network security policies; please keep in mind that we will update our NSPs later.

```sh
oc -n a3e512-tools process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=tools | oc -n a3e512-tools create -f -
oc -n a3e512-dev process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=dev | oc -n a3e512-dev create -f -
oc -n a3e512-test process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=test | oc -n a3e512-test create -f -
oc -n a3e512-prod process -f templates/nsp/nsp-deploy.yaml -p NAMESPACE=a3e512 -p TAG_NAME=prod | oc -n a3e512-prod create -f -
```

### Configuration
The *.param files in the repo are the result of generation and manual edit. However, you may find you need different values or add more parameters to your templates.  When adding more parameters, you will need to re-generate.

**Important:** The [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools) does do some internal mashing and generating, so the values in your templates may or may not end up in your *.param files as you expect or intend.

Pay particular attention to `APPLICATION_DOMAIN`. This is generated as `<component-name>-<namespace-licence-plate>-<env>-<domain-postfix>` (ex. mines-permitting-agent-a3e512-dev.apps.silver.devops.gov.bc.ca). In [settings.sh](settings.sh), we have overridden the default `APPLICATION_DOMAIN_POSTFIX` required for Openshift 4 domains. But just be aware that the value you enter for `APPLICATION_DOMAIN` in your templates will be changed on generate.

**Note:** This is one operation that did not work on Mac Mojave (did not respect `export skip_git_overrides="mines-permitting-agent-build.yaml db-build.yaml"` in `settings.sh`).

1. Review the generate params options

```sh
genParams.sh -h
```

Note the `-f` for force overwrite and `-c` to limit to a single component.

Example: force overwrite the db params.

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


### Overview of build and deployment

There are three components that need to be built and deployed:

1. agent
1. agent wallet (db)
1. issuer/controller

The agent's wallet requires registration with the ledger (Org. Book BC), and the agent itself needs to request, receive and accept an invitation to Org. Book to connect with its agent.

The issuer/controller registers its schemas through its agent.

The agent requires a callback hook to the issuer/controller.

We will use `dev` and `mines-permitting-*` for the following examples.

#### First time build and deployment
The first build and deployment into a namespace/environment require some manual intervention and startup considerations.

##### one time only tasks
We only need to build these images once (unless security and bug fixes are made to the underlying code).

1. build db image
1. build mines-permitting-agent image

##### one time per namespace/environment
We only need to do these tasks one time.  Once everything is registered and stood up, we do not want to change the encryptions and registrations.

1. generate agent secrets
1. register did with Org. Book ledger
1. tag db and mines-permitting-agent image
1. deploy mines-permitting-wallet and mines-permitting-agent
1. connect mines-permitting-agent to org. book agent via invitations

Note the label/alias for the invitation from Org. Book.  We will need to ensure our issuer uses its `CR_CONNECTION_NAME` parameter.

Another note: since we have not stood up the issuer, there will be an error in the logs after the invitation is received; this is our agent attempting to call into our (non-existent) issuer.  Ignore.

#### Ongoing build and deployment (issuer)
The issuer has the schemas for our verifiable credentials, so any updates to schemas will require builds and deploys.

1. build mines-permitting-issuer image
1. tag mines-permitting-issuer image
1. deploy mines-permitting-issuer (use the correct `CR_CONNECTION_NAME` parameter value when prompted)
1. mines-permitting-issuer self-registers its schemas with the mines-permitting-agent


#### Promotion from DEV to TEST
When promoting from DEV to TEST (and TEST to PROD), we do **NOT** build the images.

1. ensure the *.<env>.param files have the correct values
1. tag all the images required for the promotion
1. deploy the required components


### Build and Deployment commands
Again, remember the assumption that you are in your terminal at `mines-digital-trust/openshift` and logged into Openshift. We assume the housekeeping tasks complete and that the param files have been generated and verified for correctness.

#### build db image

```sh
genBuilds.sh -c db
```

#### build mines-permitting-agent image

```sh
genBuilds.sh -c mines-permitting-agent
```

#### generate agent secrets
This command generates two secrets in the dev environment. You should be prompted for four values, just hit enter and let it generate valid values.

```sh
genDepls.sh -c mines-permitting-agent-secrets -e dev
```

#### register did with Org. Book ledger
Now that we have a wallet seed, we need to register it with the ledger.  We will use the Dev instance of Org. Book as an example.

1. Go to http://dev.bcovrin.vonx.io
2. see the Authenticate a New DID panel, select Register from Seed.
3. Copy value for seed from `mines-permitting-agent-wallet-credentials-primary` secret
4. set Wallet Seed = secret value for seed
5. set Alias = mines-permitting-agent
6. click Register DID
7. Save the returned values

#### tag db and mines-permitting-agent images
Tagging the images for a namespace/environment (dev, test, prod) makes them available for deployment. Using dev as an example.

```sh
oc -n a3e512-tools tag db:latest db:dev
oc -n a3e512-tools tag mines-permitting-agent:latest mines-permitting-agent:dev
```

#### deploy mines-permitting-wallet and mines-permitting-agent
Deploy the wallet; on completion, deploy the agent.

```sh
genDepls.sh -c mines-permitting-wallet -e dev
```

```sh
genDepls.sh -c mines-permitting-agent -e dev
```

You can verify your agent is running by [checking agent connections](#-check-agent-connections)

#### connect mines-permitting-agent to org. book agent via invitations
[Port forward your agent](#port-forward-to-agent), and we can set connections via curl.

1. Send a request to the VON Team [rocketchat #von-general](https://chat.pathfinder.gov.bc.ca/channel/von-general) for an invitation to Org. Book DEV.
1. Copy the JSON they provide
1. In POSTMAN (or curl or other), POST the invitation with an alias to the Org. Book agent (`icob-agent` - see the label value in the invitation), remember to use your Admin API Key header. `/connections/receive-invitation?alias=icob-agent`
1. Using the returned value, find the `connection-id`.  POST that to `/connections/<connid>/accept-invitation`.
1. Check your connection to `icob-agent` is active.  GET `/connections/<connid>`

Using curl, assume the agent is port forwarded to 28024.

```
curl --location --request POST 'http://localhost:28024/connections/receive-invitation?alias=icob-agent' \
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

# check response for connection_id, then query your connections endpoint. We want this connection to have a state of active

curl --location --request GET 'http://localhost: 28024/connections/<connection_id>' \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <your agent-primary admin-api-key value>'
```

#### build mines-permitting-issuer image

```sh
genBuilds.sh -c mines-permitting-issuer
```

#### tag mines-permitting-issuer image
Tagging the images for a namespace/environment (dev, test, prod) makes them available for deployment. Using dev as an example.

```sh
oc -n a3e512-tools tag mines-permitting-issuer:latest mines-permitting-issuer:dev
```

#### deploy mines-permitting-issuer
This command generates a secret to hold Credential Registry (Org. Book) Administration configuration.  These are currently not used. Therefore, you can leave the prompts blank. You should be prompted for three more values related to the Org. Book, just hit ensure they are correct for your target environment.  Of particular importance is the `CR_CONNECTION_NAME`, which should match the alias used when [receiving the invitation to Org. Book](#connect-mines-permitting-agent-to-org-book-agent-via-invitations).

```sh
genDepls.sh -c mines-permitting-issuer -e dev
```

#### mines-permitting-issuer self-registers its schemas with the mines-permitting-agent
Since we have already connected our agent to Org. Book, in the logs, you should see something like the following, indicating that the connection to our agent (and it to Org. Book) is synchronized, and our issuer is registered. We can now [issue credentials](#issue-credentials) through our agent.

```sh
Starting server ...
[2021-01-14 23:00:33 +0000] [1] [INFO] Starting gunicorn 20.0.4
[2021-01-14 23:00:33 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
[2021-01-14 23:00:33 +0000] [1] [INFO] Using worker: gevent
[2021-01-14 23:00:33 +0000] [41] [INFO] Booting worker with pid: 41
Configuration variable not defined: APPLICATION_URL
Initializing app.app ...
Configuration variable not defined: ENDPOINT_URL
Configuration variable not defined: ENDPOINT_URL
Configuration variable not defined: ENDPOINT_URL
Configuration variable not defined: TOB_AGENT_ADMIN_URL
Registered issuer:  myorg
Connection cd402639-124c-481e-8028-7720ab7884df is synchronized
 acapy.events {"msg_id": "N/A", "thread_id": "N/A", "traced_type": "agent_callback.issuer_registration", "timestamp": 1610665251.3974607, "str_time": "2021-01-14 23:00:51.397461", "handler": "bcreg.controller", "ellapsed_milli": 0, "outcome": "agent_callback.issuer_registration.START"}
 acapy.events {"msg_id": "N/A", "thread_id": "N/A", "traced_type": "agent_callback.issuer_registration", "timestamp": 1610665251.3978395, "str_time": "2021-01-14 23:00:51.397840", "handler": "bcreg.controller", "ellapsed_milli": 0, "outcome": "agent_callback.issuer_registration.SUCCESS"}
```

## Code Examples

### Port forward to agent
We can verify the agent by hitting its admin port. We do not want to create a public route to the admin port, so we can use port-forwarding to connect through our local machine.

The following is an example on Mac; you may need to adjust to your particular machine.

```sh
# get a pod name
oc -n a3e512-dev get pods -o name --selector role=agent,name=mines-permitting-agent-primary
> pod/mines-permitting-agent-primary-1-22nvf
> pod/mines-permitting-agent-primary-1-zbj75

# port forward and store the process id
oc -n a3e512-dev port-forward pod/mines-permitting-agent-primary-1-22nvf 28024:8024 > /dev/null 2>&1 & AGENT_ADMIN_PORT_FORWARD_PID=$!

# run any connections/tests through POSTMAN or curl

# kill the process when you are done
kill -9 $AGENT_ADMIN_PORT_FORWARD_PID
```

### Check agent connections
Assume that we have a [port-forward](#port-forward-to-agent) open to our agent on 28024.

1. From the `mines-permitting-agent-primary` secret, copy the value for `admin-api-key`
2. check the agent connections

```sh
curl --location --request GET 'http://localhost:28024/connections' \
--header 'X-API-KEY: your key here'

# expect 200 OK with {results: []} , there are no connections yet...
```

### Issue Credentials

1. From the `mines-permitting-issuer-primary` secret, copy the value for `issuer-secret-key`
2. issue credentials

```sh
curl --location --request POST 'https://mines-permitting-issuer-a3e512-dev.apps.silver.devops.gov.bc.ca/issue-credential' \
--header 'Content-Type: application/json' \
--header 'SECRET_KEY: <your issuer-secret-key value>' \
--data-raw '[
    {
        "schema": "my-registration.bcgov-mines-permitting",
        "version": "1.0.0",
        "attributes": {
            "corp_num": "DEF67890",
            "registration_date": "2018-01-01",
            "entity_name": "Ima Regional Mining Corp",
            "entity_name_effective": "2018-01-01",
            "entity_status": "ACT",
            "entity_status_effective": "2019-01-01",
            "entity_type": "DEF",
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
        "schema": "bcgov-mines-act-permit.bcgov-mines-permitting",
        "version": "0.1.0",
        "attributes": {
            "permit_id": "MYPERMIT67890",
            "entity_name": "Ima Regional Mining Corp",
            "corp_num": "DEF67890",
            "permit_no":"MX-TEST-1",
            "mine_no":"B1000789",
            "mine_class":"regional",
            "latitude":"-49.123",
            "longitude":"-120.245",
            "issued_date": "2019-01-01",
            "effective_date": "2019-06-01",
            "authorization_end_date": "2023-01-01",
            "inspector_name": "Gadget Inspector"
        }
    }
]'
```

You should expect a result like this:

```sh
[
    {"result":"8329e996-3faa-4117-81da-4d930c7e5577","success":true},
    {"result":"28ce41b0-65f4-4ade-971e-cadd4a0eaf65","success":true}
]
```

Go to the [Org. Book](https://dev.orgbook.gov.bc.ca/en/home) and search for your entity (`Ima Regional Mining Corp`)


### Manual Cleanup scripts

Use the following carefully, and only when required (i.e. you are testing out scripts on a clean environment that is not in use).

```sh
oc -n a3e512-dev delete all,pods,services,secrets,routes,dc,pvc,hpa,nsp -l="name=mines-permitting-wallet-primary"
oc -n a3e512-dev delete all,pods,services,routes,dc,pvc,hpa,nsp -l="name=mines-permitting-agent-primary"
oc -n a3e512-dev delete secrets -l="name=mines-permitting-agent-secrets-primary"
oc -n a3e512-dev delete all,pods,services,secrets,routes,dc,pvc,hpa,nsp -l="name=mines-permitting-issuer-primary"
```

```sh
oc -n a3e512-tools delete bc,build,is,imagestreamtag -l="name=db"
oc -n a3e512-tools delete bc,build,is,imagestreamtag -l="name=mines-permitting-agent"
oc -n a3e512-tools delete bc,build,is,imagestreamtag -l="name=mines-permitting-issuer"
```
