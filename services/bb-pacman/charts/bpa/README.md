# bpa

These are abbreviated instructions used for deploying into OCP4, see the [original](./README-upstream) README for broader k8s integration. 

This chart will install a business partner agent (bpa-core & bpa-acapy) and Postgres.

It will also create the default ingress routes.

## TL;DR

This will automatically generate the wallet_seed register the new agents on the specified Indy Hyperledger ([values](./values.yaml).bpa.ledgerURL and [values](./values.yaml).bpa.ledgerBrowser)
```sh
# login to kubuernetes cluster (we are using OCP4)
# Select the target namespace
helm install bpa1 bpa
```

To update existing deployments, run this instead
``` sh
helm upgrade bpa1 bpa
```

## Introduction

This chart bootstraps a business partner agent deployment on a Kubernetes cluster using the Helm package manager. Its default installation comes with PostgreSQL. Ingress can be activated, allowing the agent to communicate with other agents outside the cluster.

## Requirements

- Kubernetes 1.12+
- Docker
- Helm v3.3.4+
- PV provisioner support in the underlying infrastructure (for PostgreSQL persistence)
- If activating Ingress:
  - Ingress controller installed
  - Cert-manager
  - DNS records pointing to your routes 


#### Install multiple bpa instances

> You could easily deploy a second business partner agent like this, e.g. for demo purpose.
> Just use a different helm release name.


## Registering Secret Prior to Startup

- If you want to define the seed, you can create the secret <.Release.Name>-acapy {seed: <SEED>}


- If you need to register your DID manually prior to starting the BPA (required for Sovrin MainNet)

  - start app targetting a ledger that is free to write to, grab did/verkey and register those same values on the restricted ledger
  - start agent and call the acapy admin api's `wallet/did/public` to get the values, register them, and restart the app.


## Uninstalling the Chart

**This also deletes the secret that holds the SEED used to create and register it's DID. if you run uninstall/delete on the helm chart, you will need to either, SAVE the seed in the secret somewhere else to re-use it in the following installation, OR, also delete the PVC so both can be recreated.**


To uninstall/delete the my-release deployment:

```sh
helm delete mybpa
```

The command removes all the Kubernetes components but PVC's associated with the chart and deletes the release. 
To delete the PVC's associated with my-release:

```sh
kubectl delete pvc -l release=mybpa
```

Note: Deleting the PVC's will delete postgresql data as well. Please be cautious before doing it.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| acapy.adminURLApiKey | string | `"2f9729eef0be49608c1cffd49ee3cc4a"` |  |
| acapy.affinity | object | `{}` |  |
| acapy.agentName | string | `"ca-aca-py"` |  |
| acapy.agentSeed | String | `nil` | The agent seed, 32 characters. See main documentation.  |
| acapy.fullnameOverride | string | `""` |  |
| acapy.image.pullPolicy | string | `"IfNotPresent"` |  |
| acapy.image.repository | string | `"bcgovimages/aries-cloudagent"` |  |
| acapy.image.tag | string | `"py36-1.15-0_0.5.6"` | Overrides the image tag whose default is the chart appVersion. |
| acapy.imagePullSecrets | list | `[]` |  |
| acapy.ingress.annotations | object | `{}` |  |
| acapy.ingress.enabled | bool | `false` |  |
| acapy.ingress.hosts[0].host | string | `"my-acapy.local"` |  |
| acapy.ingress.hosts[0].paths | list | `[]` |  |
| acapy.ingress.tls | list | `[]` |  |
| acapy.name | string | `"acapy"` |  |
| acapy.nameOverride | string | `""` |  |
| acapy.nodeSelector | object | `{}` |  |
| acapy.podAnnotations | object | `{}` |  |
| acapy.podSecurityContext | object | `{}` |  |
| acapy.readOnlyMode | bool | `false` |  |
| acapy.resources | object | `{}` |  |
| acapy.securityContext | object | `{}` |  |
| acapy.service.adminPort | int | `8031` |  |
| acapy.service.httpPort | int | `8030` |  |
| acapy.service.type | string | `"ClusterIP"` |  |
| acapy.tolerations | list | `[]` |  |
| bpa.affinity | object | `{}` |  |
| bpa.agentName | string | `"Business Partner Agent"` | The Agent Name as it should be displayed in the UI |
| bpa.didPrefix | string | `"did:sov:iil:"` | The ledger prefix that is configured with the Uni Resolver |
| bpa.image.pullPolicy | string | `"IfNotPresent"` |  |
| bpa.image.repository | string | `"ghcr.io/hyperledger-labs/business-partner-agent"` |  |
| bpa.image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| bpa.imagePullSecrets | list | `[]` |  |
| bpa.ingress.annotations | object | `{}` |  |
| bpa.ingress.enabled | bool | `false` |  |
| bpa.ingress.hosts[0].host | string | `"my-bpa.local"` |  |
| bpa.ingress.hosts[0].paths | list | `[]` |  |
| bpa.ingress.tls | list | `[]` |  |
| bpa.ledgerBrowser | string | `"https://indy-test.bosch-digital.de"` | The Ledger Explorer   |
| bpa.ledgerURL | string | `"https://indy-test.bosch-digital.de"` | The Ledger URL |
| bpa.name | string | `"bpacore"` |  |
| bpa.nodeSelector | object | `{}` |  |
| bpa.password | string | `"changeme"` | Default password, overwrite default if running in production like environments |
| bpa.podAnnotations | object | `{}` |  |
| bpa.podSecurityContext | object | `{}` |  |
| bpa.resolverURL | string | `"https://resolver.stage.economyofthings.io"` | Uni Resolver URL |
| bpa.resources | object | `{}` |  |
| bpa.schemas.bankaccount.id | string | `"M6Mbe3qx7vB4wpZF4sBRjt:2:bank_account:1.0"` |  |
| bpa.schemas.commercialregister.id | string | `"3gLVpb3i5jzvZqWYyesSB3:2:commercialregister:1.2"` |  |
| bpa.securityContext | object | `{}` |  |
| bpa.securityEnabled | bool | `true` | enable security (username and password) |
| bpa.service.port | int | `80` |  |
| bpa.service.type | string | `"ClusterIP"` |  |
| bpa.tolerations | list | `[]` |  |
| bpa.userName | string | `"admin"` | Default username |
| bpa.webMode | bool | `false` | Run in did:web mode with read only ledger. If set to true acapy.readOnlyMode has to be true too. |
| global.fullnameOverride | string | `""` |  |
| global.nameOverride | string | `""` |  |
| global.persistence.deployPostgres | bool | `true` | If true, the Postgres chart is deployed |
| postgresql.image.tag | int | `12` |  |
| postgresql.persistence | object | `{"enabled":false}` | Persistent Volume Storage configuration. ref: https://kubernetes.io/docs/user-guide/persistent-volumes |
| postgresql.persistence.enabled | bool | `false` | Enable PostgreSQL persistence using Persistent Volume Claims. |
| postgresql.postgresqlDatabase | string | `"bpa"` | PostgreSQL Database to create. |
| postgresql.postgresqlPassword | string | `"change-me"` | PostgreSQL Password for the new user. If not set, a random 10 characters password will be used. |
| postgresql.postgresqlUsername | string | `"bpa"` | PostgreSQL User to create. |
| postgresql.service | object | `{"port":5432}` | PostgreSQL service configuration |

## Chart dependencies
| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami/ | postgresql | 10.1.3 |

## Chart development

### Publish chart(s)

See [publishing docu](../../PUBLISHING.md).

### Documentation

The chart documentation is generated via `helm-docs` out of a go template.

```sh
cd charts
docker run --rm --volume "$(pwd):/helm-docs" -u $(id -u) jnorwood/helm-docs:latest
```

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Frank Bernhardt | Frank.Bernhardt@bosch.com |  |
| Jason Syrotuck  | Jason.Syrotuck@nttdat.com |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.4.0](https://github.com/norwoodj/helm-docs/releases/v1.4.0)