[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![img](https://img.shields.io/badge/Lifecycle-Experimental-339999)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)
[![Maintainability](https://api.codeclimate.com/v1/badges/1f62bd5e189348d05432/maintainability)](https://codeclimate.com/github/bcgov/mines-digital-trust/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1f62bd5e189348d05432/test_coverage)](https://codeclimate.com/github/bcgov/mines-digital-trust/test_coverage)

# Mines-Digital-Trust, Permit Issuer/Controller for Aries VCR

This repository is based on the [Aries VCR Issuer Controller template](https://github.com/bcgov/aries-vcr-issuer-controller) for creating an [Aries](https://www.hyperledger.org/use/ARIES) Verifiable Credential Registry (VCR) Issuer Agent. [Aries VCR](https://github.com/bcgov/aries-vcr) is the foundational technology upon which the Government of British Columbia's [OrgBookBC](https://orgabook.gov.bc.ca) was built. Aries VCR Issuer Controller is a starter kit for building an Aries agent that issues verifiable credentials to instances of an Aries VCR, such as OrgBookBC. This repo contains code for an issuer controller that works with [Aries Cloud Agent Python](https://github.com/hyperledger/aries-cloudagent-python) (ACAPy) framework. The controller and an instance of ACA-Py can be deployed together to implement an Aries issuer agent.

`aries-vcr-issuer-controller` was developed as part of the Verifiable Organizations Network (VON). For more information on VON, visit https://vonx.io.  Even better, join in with what we are doing and contribute to VON and the [Trust over IP](trustoverip.org) community.

Still not sure what this is? Please see this [Getting started with VON](https://vonx.io/getting_started/get-started/) overview, paying particular attention to the `VON Issuer/Verifier Agent` section. That's what this repo implements.

## Terminology

### Permit Issuer/Controller or Agent

Aries Agents consist of two parts, a framework that handles all of the Aries agent type functions (e.g. messages, protocols, protocol state, agent storage, etc.) and a controller that provides the business logic that gives the agent personality. As such, we talk about the code in this repo as the Controller. When the controller code is deployed along with an instance of an agent framework&mdash;ACA-Py&mdash;we have an Aries VCR Issuer agent.  As such, in this repo we might talk about the code in this repo (the Permit Issuer/Controller), or talk about a deployed and running Aries VCR Issuer Agent.

Make sense?

### Aries VCR vs. OrgBook

A question we often get is what's the difference between OrgBook and Aries VCR? Here are the details.

The OrgBook is a specific instance of Aries VCR about registered organizations within a legal jurisdiction (e.g. province, state or nation). Each entity in an OrgBook is a registered organization (a corporation, a sole proprietorship, a co-op, a non-profit, etc.), and all of the verifiable credentials within an OrgBook repository relate to those registered organizations.

So while OrgBook is an instance of the Aries VCR software, Aries VCR itself knows nothing about jurisdictions, registered organizations, etc. As a result can be used in many credential registry use cases. If the entities within an Aries VCR instance were doctors, then the verifiable credentials would all be about those doctors, and we'd have "DocBook". Same with engineers, lawyers, teachers, nurses and more. If an Aries VCR instance had construction sites as top level entities, the verifiable credentials would all be about those construction sites, such as permits, contractors, contracts, payments and so on.

Aries VCR knows about verifiable credentials, how to hold them, prove them and how to make the available for searching based on the values in the claims. What is in those credentials is up to the issuers that issue to that instance of an Aries VCR.

We often talk about the OrgBook being a repository of public credentials, and that OrgBook is publicly searchable. However, instances of Aries VCR do not have to contain public credentials and the website does not have to be publicly accessible. An organization could implement an instance of an Aries VCR, load it with with credentials containing proprietary data and wrap it with a mechanism to allow only authorized entities to access the data.

## Getting Started

Use this [Permit Issuer/Controller Getting Started Tutorial](GettingStartedTutorial.md) to go through the basics of running the Permit Issuer Agent created from the Aries VCR Issuer Controller template.

## Configuration Guide

Much of the work in configuring an the Permit Issuer Agent is in setting up the YAML files in the [services/ghg-orgbook-issuer-controller/config](services/ghg-orgbook-issuer-controller/config) folder. A [Configuration Guide](services/ghg-orgbook-issuer-controller/config/README.md) documents those files.

## Getting Help or Reporting an Issue

To report bugs/issues/feature requests, please file an [issue](../../issues).

# How to Contribute

If you find this project helpful, please contribute back to the project. If you would like to contribute, please see our [CONTRIBUTING](./CONTRIBUTING.md) guidelines. Please note that this project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

# Business to Business Credential Manager

The Business to Business Credential Manager is software run by an organization for issuing, holding, and verifying digital trust credentials. Supported by blockchain technology, organizations can share and receive proofs that are secure and verifiable.

## **Who can use it?**

Any organization who wants to participate in the digital trust ecosystem by issuing, holding, and verifying verifiable credentials can use the Business to Business Credential Manager. For example, government, company, third-party, etc.

## **How does it work?**

To understand the big picture, let's start with talking about the key concepts.

- **Decentralized Identifier (DID)**: Defined by the W3C DID specification, a DID is:
  - Is globally unique
  - Can identify any subject (e.g. an organization, person, credential, transaction, etc.)
  - Is associated with exactly one subject
- **Verifiable Credential**: Similar to the driver's license you hold in your wallet, which you can use to prove your identity to a police officer, a company can be issued a registration credential from a trusted source like BC Registries. What makes a credential "verifiable"?
  - Can validate the issuer and holder of a credential
  - Can confirm the credential is not revoked
  - Can prove the credential has not changed
- **Wallet**: Verifiable credentials can be stored in a digital wallet. In many ways it is just like your physical one. This is where you store your organization's information that you will use to prove to other organizations that you hold a certain credential.
- **Proof Request**: A proof request is the message sent by the relying party to the holder describing the verifiable attributes and appropriate conditions (e.g. predicates, issuer of attributes, schema of the credentials used, etc.) that the holder needs to satisfy.

Now let's see some generic use cases.

- **Issuing and Holding Verifiable Credential**
  1. The *Issuer organization* imports or creates  a schema for the type of verifiable credential it wants to issue.
  2. The *Issuer organization* and *Holder organization* make a connection via their Business to Business Credential Managers.
  3. The *Issuer organization* issues a credential following the credential definition created from the schema to the *Holder organization*.
  4. The *Holder organization* receives the verifiable credential and stores it in its wallet.
- **Verifying Credential**
  1. The *Verifier organization* imports or creates  a template for the proof request it wants to send.
  2. The *Verifier organization* and *Holder organization* make a connection via their Business to Business Credential Managers.
  3. The *Verifier organization* sends a proof request using the predefined proof request template to the *Holder organization*.
  4. The *Holder organization* receives the proof request and presents the proof by disclosing chosen verifiable credentials and/or chosen attribute values of the verifiable credentials it holds in its wallet to the *Verifier organization*.

## Terms & Definitions in the UI

- **Dashboard**:
- **Profile**:
- **Wallet**:
  - **Credentials**:
  - **Credential Attribute**:
- **Credential Management**:
  - **Credential Schema**:
  - **Credential Definition**:
- **Proof Requests**:
  - **Proof Request Template**:
- **Connections**:
  - **Business Connection**:
  - **Network**:
  - **Connection Request**:
  - **Connection Invitation QR Code**:
- **Notifications**:
