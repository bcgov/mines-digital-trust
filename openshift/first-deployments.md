# First Time Deployment
This document guides you through the first time deployment into a namespace/environment.  The first time deployment is very hands on and requires a few out-of-band steps and coordination with the Org. Book team.

## Prerequisites

1. You have read through this document's parent [readme](./README.md)
1. You have installed and setup your [tooling](./tooling.md)
1. Someone has [initialized](./initialization.md) the namespaces
1. Someone has [generated](./generated-params.md) deployment parameter files
1. You have read through this document!

### Assumptions

1. You have administrator permissions to your four project namespaces (*-dev, *-test, *-prod, *-tools)
1. Your terminal session is logged into Openshift and your working directory is `mines-digital-trust/openshift` (location of this file)

### Notes about examples

1. All http(s) requst examples will be in [curl](https://curl.se)
1. All examples will use the namespace licence plate: `a3e512`
1. All examples will use the `dev` environment (`a3e512-dev`), replace `dev` and `a3e512-dev` when appropriate
1. All examples will use the `mines-permitting-*` for the agent/wallet/issuer

## Overview
There are three components that need to be built and deployed:

1. agent
1. agent wallet (db)
1. issuer/controller

The agent's wallet requires registration with the ledger (Org. Book BC), and the agent itself needs to request, receive and accept an invitation to Org. Book to connect with its agent.

The issuer/controller registers its schemas through its agent.

The agent requires a callback hook to the issuer/controller (via `WEBHOOK_URL` parameter/environment variable).


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

Another note: since we have not stood up the issuer, there will be an error in the logs after the invitation is received; this is our agent attempting to call into our (non-existent) issuer; ignore this error.

#### stand up the issuer
The issuer has the schemas for our verifiable credentials, so any updates to schemas will require builds and deploys.

1. build mines-permitting-issuer image
1. tag mines-permitting-issuer image
1. deploy mines-permitting-issuer (use the correct `CR_CONNECTION_NAME` parameter value when prompted)
1. mines-permitting-issuer self-registers its schemas with the mines-permitting-agent

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

This command generates a secret in the environment. You should be prompted for one value, just hit enter and let it generate valid value for our `ISSUER_SECRET_KEY`.

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
1. ensure you have a valid `registration_id` for your Org. Book environment (the target company)
2. issue credentials

```sh
curl --location --request POST 'https://mines-permitting-issuer-a3e512-dev.apps.silver.devops.gov.bc.ca/issue-credential' \
--header 'Content-Type: application/json' \
--header 'Issuer-Secret-Key: <your issuer-secret-key value>' \
--data-raw '[
    {
        "schema": "bcgov-mines-act-permit.bcgov-mines-permitting",
        "version": "0.2.0",
        "attributes": {
            "permit_id": "MYPERMIT12345",
            "registration_id": "BC0306430",
            "permit_no": "MX-TEST-1",
            "mine_no": "B1000789",
            "mine_class": "regional",
            "latitude": "-49.123",
            "longitude": "-120.245",
            "issued_date": "2019-01-01",
            "effective_date": "2019-06-01",
            "authorization_end_date": "2023-01-01",
            "inspector_name": "Best Inspector"
        }
    }
]'
```
