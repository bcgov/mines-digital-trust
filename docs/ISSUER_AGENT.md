# Issuer/Controller for Aries VCR  

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![img](https://img.shields.io/badge/Lifecycle-Experimental-339999)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)
[![Maintainability](https://api.codeclimate.com/v1/badges/1f62bd5e189348d05432/maintainability)](https://codeclimate.com/github/bcgov/mines-digital-trust/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1f62bd5e189348d05432/test_coverage)](https://codeclimate.com/github/bcgov/mines-digital-trust/test_coverage)

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

To report bugs/issues/feature requests, please file an issue [here](https://github.com/bcgov/mines-digital-trust/issues).

## How to Contribute

Collaborations are highly appreciated, please follow the [guidelines](./CONTRIBUTING.md) if you are interested in contributing. (Please note that this project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.)

We would love to hear from you! Join us on [Rocket.chat](https://developer.gov.bc.ca/Steps-to-join-Rocket.Chat) now, we will be waiting for you at the [Mines Digital Trust](https://go.rocket.chat/invite?host=chat.developer.gov.bc.ca&path=invite%2FcS7ArW) channel. 👍
