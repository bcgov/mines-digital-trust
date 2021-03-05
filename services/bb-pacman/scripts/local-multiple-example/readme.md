# Local Multiple Example
This is a walkthrough for standing up 3 Business Partner Agents and a Universal DID Resolver locally using Docker.

Assumptions are:
- you have Docker installed
- you can run Docker compose
- you understand VON, aca-py, and all the related technologies.

This is also a very particular example where we are using an external ledger for the British Columbia Government (`http://test.bcovrin.vonx.io`). You can stand up your own local VON network (or connect to the ledger of your choice), but you will have to build your own Resolver. Follow the steps and review the repositories in the DID Resolver section to get some leads on how to stand up your own Resolver. You will need the Genesis transactions for your ledger. 


The local network makes use of the docker internal networking resolution (`host.docker.internal`). If you are running on a Linux machine, you may need to pass in additional command line configuration:

```bash
docker-compose up --add-host=host.docker.internal:host-gateway
```

The example environments for the BPAs and Resolver use the following Ports locally. Ensure you have no conflicts and change as necessary.

| Component | Reason | Port |
| --- | --- | --- |
| Resolver | Resolver/Ledger | 7777 |
|  | DID Sov | 7776 |
| BPA 1 | Web | 18080 |
|  | ACA Py Agent | 18030 |
| --- | ACA Py Admin | 18031 |
| --- | Wallet DB | 15432 |
| BPA 2 | Web | 28080 |
|  | ACA Py Agent | 28030 |
| --- | ACA Py Admin | 28031 |
| --- | Wallet DB | 25432 |
| BPA 3 | Web | 38080 |
|  | ACA Py Agent | 38030 |
| --- | ACA Py Admin | 38031 |
| --- | Wallet DB | 35432 |


## DID Resolver
This example is building a local image for running against the `http://test.bcovrin.vonx.io` ledger. 

### Build Images
First clone and build the sovrin resolver (for bcovrin test):

 ```bash
 git clone https://github.com/ianco/uni-resolver-driver-did-sov.git
 cd uni-resolver-driver-did-sov
 docker build -f ./docker/Dockerfile . -t universalresolver/driver-did-sov
 ```

 Now run the universal resolver (the only profile is for our bcovrin resolver)

 ```bash
 git clone https://github.com/ianco/universal-resolver.git
 cd universal-resolver
 docker pull universalresolver/uni-resolver-web:latest
 ```
Now you have a very slimmed down resolver image that can find DIDs on the network. 

**IMPORTANT:** Ensure the resolver is running before standing up the Business Partner Agents.
  
### Run
Open a separate terminal window, navigate to [resolver](./resolver).
 
```bash
docker-compose up
```
  
### Test
Open a separate terminal window, navigate to [resolver](./resolver).
 
```bash
curl -X GET http://localhost:7777/1.0/identifiers/did:sov:MTMagrM95WXayAHfwTNY17
```
  
### Stop
Open a separate terminal window, navigate to [resolver](./resolver).
 
```bash
docker-compose down
```

### Teardown
Open a separate terminal window, navigate to [resolver](./resolver).
 
```bash
docker-compose down -v --remove-orphans
```

### Business Partner Agents
Ok, now you have your DID Resolver running, you need to stand up some agents. 

Key items of note for the agent configuration are:
- the ports (mentioned above)
- `BPA_RESOLVER_URL` and `BPA_LEDGER_BROWSER` - set to your local resolver
- `BPA_DID_PREFIX`, set to `did:sov:`
- `BPA_SCHEMA_BANK_ID` and `BPA_SCHEMA_COMREG_ID`, currently set to a value on the ledger
- `ACAPY_GENESIS_URL` - set to the same ledger as the resolver
- `ACAPY_SEED` - need to generate a new one and register it for each new agent
- `AGENT_NAME` update this if you want a different name
- `BPA_BOOTSTRAP_UN` and `BPA_BOOTSTRAP_PW` change these credentials *_before_* your initial start to override the default login (`admin`/`changeme`) 

**NOTE:** the following examples were done on a Mac, please adjust as required by your operating system.

#### Build the Agent Image
We have made some code changes to run this locally successfully. You will need to build a new local version of the BPA image.

Open a separate terminal window, navigate to [business-partner-agent](../../).

```sh
docker build -t ghcr.io/hyperledger-labs/business-partner-agent:local .
```

In our examples, we will use this as our BPA Image.  

#### Start Agent 1
Open a separate terminal window, navigate to [example-1](./example-1).

Basic steps:
1. create an `.env` file
2. register agent on ledger
3. run the agent


```bash

cp .env-example .env

LEDGER_URL=http://test.bcovrin.vonx.io SRC_FILE=$(pwd)/.env-example DEST_FILE=$(pwd)/.env ../../register-did.sh

cp ../../acapy-static-args.yml .

docker-compose up
```

**NOTE:** if there are issues with the `register-did.sh` updating the `ACAPY_SEED` in the `.env` file, do it manually... copy the value for seed from the output into your file.

```sh
{
  "did": "WrdBKAVUGqXYJ99rB2yx5r",
  "seed": "V1xKxLj4Qe5qh7b8Q08t5igpO3EICuQE",
  "verkey": "HGo3Mc7i4vKw96Hh9KJ1dnn1JJazb2QLfoA7ApKqBWp6"
}
Registration on http://test.bcovrin.vonx.io successful
```

You shouldn't have to adjust your `.env` files or register unless you completely tear down your agent. Just ensure the first time you stand up your agent, that you do complete the registration process.  

##### Run
If you are running on linux, don't forget to `--add-host=host.docker.internal:host-gateway`
 
```bash
docker-compose up
```

##### (Basic) Test
Open a browser, hit the designated web port for your BPA (`18080`), and login (`admin`/`changeme` by default).


##### Stop
 
```bash
docker-compose down
```

##### Teardown
 
```bash
docker-compose down -v --remove-orphans
```

#### Start Agent 2 and 3
Follow the instructions for starting Agent 1, but navigate your terminals to [example-2](./example-2) and [example-2](./example-2) respectively. The (Basic) Test ports will be `28080` and `38080` by default (respectively).

### Schemas
These initial examples are configured with schemas and credential definitions that have already been created. If you are running on a different ledger, you will need to stand up an agent and create them. There is no UX in the BPA to do this, so we use the agent admin's [swagger UX](http://localhost:18031).

If you create new schemas - or new versions, you will need to set environment variables for you agents and restart.

- `BPA_SCHEMA_BANK_ID`
- `BPA_SCHEMA_COMREG_ID`

The version numbers are arbitrary but important for specifying the credential defintitions and issuing credentials.

Use this as a guide only, do not use expect the same `schema_id`.

#### Bank Account Schema
Create the schema/version, and record the result. You will need the schema id (to update `.env` files and create credential definitions).

`POST /schemas`

```json
{
  "attributes": [
      "bic",
      "iban"
  ],
  "schema_name": "bank_account",
  "schema_version": "1.3"
}
```

#### Commercial Registry Schema
Create the schema/version, and record the result. You will need the schema id.

`POST /schemas`

```json
{
  "attributes": [
      "companyAddressPostalCode",
      "registrationNumber",
      "companyAddressLocality",
      "companyAddressCountry",
      "companyName",
      "nominalCapital",
      "lastEntryDate",
      "did",
      "authorizedOfficers",
      "validUntil",
      "companyAddressStreet",
      "validFrom"
  ],
  "schema_name": "commercialregister",
  "schema_version": "1.3"
}
```
   
### Connect Business Agents
When the DID Resolver and the 3 Business Agents are all stood up correctly, we can connect our business agents. Currently there appears to be an issue with the actual connection (at least using the `http://test.bcovrin.vonx.io` ledger).

#### Example
In this example, we will use BPA 1 to initiate connections with BPA 2.  

1. Login to [BPA 1](http://localhost:18080) and setup a Public Profile
2. New browser, login to [BPA 2](http://localhost:28080) and setup a Public Profile
3. BPA 2, navigate to Dashboard, copy the DID.
4. BPA 1, navigate to Business Partners, click Add, Paste BPA 2 DID and click Lookup Partner
5. Review the Public Profile for BPA 2, click Add Partner
6. Open the Business Partners in BPA 1, active lights should be green, DID in top right corner should be the public DID of the partner.
7. Navigate to BPA 2, open Business Partners, there should be an entry from `Business Partner Agent 1`, but note the DID - it is incorrect, see [ACA-py Issue](https://github.com/hyperledger/aries-cloudagent-python/issues/358)

##### Fix connection

The initiating BPA has a valid connection (has the correct public DID for the partner). The receiver does not have the correct public DID for the partner. We need to pop into the database and adjust.  

This example is for BPA 2 correcting the connection initiated by BPA 1.

1. Open a connection to the target BPA 2 postgres database (port `25432`) and `walletuser` database (`walletuser`/`walletpassword`) - use your favourite method
2. Review the record in the `partner` table, the `did` field will reflect what currently seen on BPA 2's connection to BPA 1, the incorrect value
3. Copy the BPA 1's public DID (from their Dashboard screen)
4. Update the `partner`.`did` data
5. Commit the change
6. Navigate to BPA 2 Business Parters, select `Business Partner Agent 1` 7. Note the DID is now BPA 1's public DID, click `Refresh profile from source`
7. You should see BPA 1's public profile.  Update the "name" of your agent if you like (click the pencil)

You must repeat this process for all recipient BPAs.

###### Add other relationships
Now that BPA 1 is connected to BPA 2, make the other connections (BPA 1 to 3, BPA 2 to 3). Remember to fix the connection data in the database.

### Issue Credentials
In this example, we will use BPA 1 as an issuer and issue a `Bank Account Credential` and a `Commercial Register Credential` to BPA 2. There is no UX in the BPA code to issue the credential, so we will use BPA 1 agent admin's [swagger UX](http://localhost:18031).

You will need the Schema IDs (see above if you created it, and check your `.env` files).

#### Create Credential Definitions

**IMPORTANT:** at this time, do not allow revocation of credentials (we want to keep this simple).

Login to BPA 1 [swagger UX](http://localhost:18031)

`POST /credential-definitions`

```json
{
  "revocation_registry_size": 1000,
  "schema_id": "UddsJpBYawZuKoREVGETps:2:bank_account:1.3",
  "support_revocation": false,
  "tag": "default"
}
```

##### Response

```json
{
  "credential_definition_id": "HXDgnenVu9Qe8mrdoY8q7x:3:CL:107973:default"
}
```

Record the Credential Definition Id, this is what we use when issuing a credential.  


`POST /credential-definitions`

```json
{
  "revocation_registry_size": 1000,
  "schema_id": "UddsJpBYawZuKoREVGETps:2:commercialregister:1.3",
  "support_revocation": false,
  "tag": "default"
}
```

##### Response

```json
{
  "credential_definition_id": "HXDgnenVu9Qe8mrdoY8q7x:3:CL:107906:default"
}
```

Record the Credential Definition Id, this is what we use when issuing a credential.  


#### Issue Credentials
For this, you will need the `connection_id` from BPA 1. 


1. Use swagger [connection/get_connections](http://localhost:18031/api/doc#/connection/get_connections), identitfy the correct connection (by `did` or `alias`) and record the `connection_id` for the next step.


You will need:
- `cred_def_id` - see above
- `connection_id` - BPA 1's connection id to partner BPA 2
- `issuer_did`: BPA 1's DID (remove the `did:sov:` prefix),
- `schema_id`: schema id for "commercialregister" or "bank_account",
- `schema_issuer_did`: first part of the schema id (this is who created the schema),
- `schema_name`: "commercialregister" or "bank_account"
- `schema_version`: "1.3" (or whatever it is for the credential definition)

##### Commercial Register

The following is an example of issuing a "commercialregister" credential. All the ids will need to be updated appropriately; they are left as an aid to help you craft your particular issuance request.

Login to BPA 1 [swagger UX](http://localhost:18031)


`POST /issue-credential/send`

```json
{
  "auto_remove": true,
  "comment": "string",
  "connection_id": "22e7bfef-10e9-4e5c-8a77-5925da9d3dfc",
  "cred_def_id": "HXDgnenVu9Qe8mrdoY8q7x:3:CL:107906:default",
  "credential_proposal": {
    "@type": "issue-credential/1.0/credential-preview",
    "attributes": [
      {
        "name": "did",
        "value": "22222222222222222"
      },
      {
        "name": "validFrom",
        "value": "2021-01-01"
      },
      {
        "name": "validUntil",
        "value": "2021-12-31"
      },
      {
        "name": "companyName",
        "value": "Second Co."
      },
      {
        "name": "lastEntryDate",
        "value": "2021-02-02"
      },
      {
        "name": "nominalCapital",
        "value": "2222222"
      },
      {
        "name": "authorizedOfficers",
        "value": "CEO"
      },
      {
        "name": "registrationNumber",
        "value": "222"
      },
      {
        "name": "companyAddressStreet",
        "value": "222 Second St"
      },
      {
        "name": "companyAddressCountry",
        "value": "Canada"
      },
      {
        "name": "companyAddressLocality",
        "value": "BC"
      },
      {
        "name": "companyAddressPostalCode",
        "value": "BBB222"
      }
    ]
  },
  "issuer_did": "HXDgnenVu9Qe8mrdoY8q7x",
  "schema_id": "UddsJpBYawZuKoREVGETps:2:commercialregister:1.3",
  "schema_issuer_did": "UddsJpBYawZuKoREVGETps",
  "schema_name": "commercialregister",
  "schema_version": "1.3",
  "trace": true
}
```

Login to [BPA 2](http://localhost:28080), you should see an indicator that something has been added to the wallet! Open the credential, and add to the public profile.

##### Bank Account

The following is an example of issuing a "bank_account" credential. All the ids will need to be updated appropriately; they are left as an aid to help you craft your particular issuance request.

Login to BPA 1 [swagger UX](http://localhost:18031)


`POST /issue-credential/send`

```json
{
  "auto_remove": true,
  "comment": "string",
  "connection_id": "22e7bfef-10e9-4e5c-8a77-5925da9d3dfc",
  "cred_def_id": "HXDgnenVu9Qe8mrdoY8q7x:3:CL:107973:default",
  "credential_proposal": {
    "@type": "issue-credential/1.0/credential-preview",
    "attributes": [
      {
        "name": "bic",
        "value": "222222222222222"
      },
      {
        "name": "iban",
        "value": "2222-2222-222-2"
      }
    ]
  },
  "issuer_did": "HXDgnenVu9Qe8mrdoY8q7x",
  "schema_id": "UddsJpBYawZuKoREVGETps:2:bank_account:1.3",
  "schema_issuer_did": "UddsJpBYawZuKoREVGETps",
  "schema_name": "bank_account",
  "schema_version": "1.3",
  "trace": true
}
```

Login to [BPA 2](http://localhost:28080), you should see an indicator that something has been added to the wallet! Open the credential, and add to the public profile.

You should repeat this issuing credentials to BPA 3; you will not need to create new credential definitions for BPA 1 to issue.


#### Proofs

Now BPA 2 and BPA 3 have 2 credentials on their public profiles. We will exchange proofs.

First, we will get BPA 2 to request a proof from BPA 1 for their Commercial Register.

1. Login to [BPA 2](http://localhost:28080)
2. Go to Settings, enable Expert mode
3. Go to Business Partners, select BPA 3
4. Refresh their profile, you should now see Verified Credentials issued to BPA 3
5. Click Request Presentation, paste in the Cred Def for Commercial Register
6. It may take a bit, you will need to refresh BPA 2's Business Partners, but the request should end up being marked as successful.

**NOTE:** Unclear if bug or intended feature, but BPA 3 does not indicate that is has sent a presentation to BPA 2 (even though BPA 2 has received a proof)

Let's have BPA 3 request a proof of Bank Account from BPA 2.

1. Login to [BPA 3](http://localhost:38080)
2. Go to Settings, enable Expert mode
3. Go to Business Partners, select BPA 2
4. Refresh their profile, you should now see Verified Credentials issued to BPA 2
5. Click Request Presentation, paste in the Cred Def for Bank Account
6. It may take a bit, you will need to refresh BPA 3's Business Partners, but the request should end up being marked as successful.

Now let's have BPA 2 present a proof of Commercial Register to BPA 3.

1. Login to [BPA 2](http://localhost:28080)
2. Go to Business Partners, select BPA 3
3. Click Send Presentation, you should see a list credentials to send, select Commercial Register, click Submit
6. It may take a bit, you will need to refresh BPA 2's Business Partners, but the send should end up being marked as successful.

In this case, when we return to BPA 3, the Send from BPA 2 is listed in BPA 3's Received...

Now, let's present a Bank Account proof from BPA 3 to 2.

1. Login to [BPA 3](http://localhost:38080)
2. Go to Business Partners, select BPA 2
3. Click Send Presentation, you should see a list credentials to send, select Bank Account, click Submit
6. It may take a bit, you will need to refresh BPA 3's Business Partners, but the send should end up being marked as successful.

### Great Success!!!
Hopefully, you have arrived here with no problems.  3 Business Partner Agents have established connections with each other using their public DIDs.  1 BPA has issued credentials to the other 2 and the 2 credential holders have exchanged proofs either through proof requests or proof proposals being sent.



