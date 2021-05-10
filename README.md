[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![img](https://img.shields.io/badge/Lifecycle-Experimental-339999)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)
[![Maintainability](https://api.codeclimate.com/v1/badges/1f62bd5e189348d05432/maintainability)](https://codeclimate.com/github/bcgov/mines-digital-trust/maintainability)

# Introduction

The Mines Digital Trust POC was initiated by the BC Ministry of Energy, Mines and Low Carbon Innovation to support:

- producers of consumer goods and purchasers of mineral resources in proving responsible sourcing;
- government in exploring the community effort to establish a digital trust ecosystem for finding, issuing, storing, and sharing trustworthy data via verifiable credentials.

Our team has build 2 common services by leveraging common components:

## Service I - Issuing Verifiable Credentials to OrgBook BC

Verifiable credentials for Mines Act Permits and any related observable data metrics of a mine site can be issued to [OrgBook BC](https://www.orgbook.gov.bc.ca/en/home) via this common service. Learn more about issuing verifiable credentials to OrgBook BC [here](./ISSUER_AGENT.md) now.

### Components:

- [Trust Over IP stack](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0289-toip-stack)
  - Issuer Agent
  - Issuer Controller
  - [Hyperledger Aries Cloud Agent Python](https://github.com/hyperledger/aries-cloudagent-python)
  - Client API Wrapper
- [Aries Verifiable Credentials Registry Instance (OrgBook BC)]( https://github.com/bcgov/aries-vcr)

## Service II - Business to Business Credential Manager

The Business to Business Credential Manager (BBCM) is software run by an organization for issuing, holding, and verifying digital trust credentials. Powered by [Hyperledger](https://www.hyperledger.org/), with BBCM organizations can share and receive proofs that are secure and verifiable. Want to become an early adopter? Learn more about it [here](./BBCM.md) now.

### Components:

- [Business Partner Agent](https://github.com/hyperledger-labs/business-partner-agent)
  - Connection Manager - For establishing connection between 2 Business Partner Agents
  - Credential Manager - For tracking and managing credentials
  - Proof Manager - For tracking and managing proof requests and presentations
  - Attestation Manager
  - Profile Manager - For managing organizational profiles
- [Hyperledger Aries Cloud Agent Python](https://github.com/hyperledger/aries-cloudagent-python)
- [Verifiable Credential Authentication with OpenID Connect](https://github.com/bcgov/vc-authn-oidc(edited))

# Getting Help or Reporting an Issue

To report bugs/issues/feature requests, please file an issue [here](https://github.com/bcgov/mines-digital-trust/issues).

# How to Contribute

Collaborations are highly appreciated, please follow the [guidelines](./CONTRIBUTING.md) if you are interested in contributing. (Please note that this project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.)

We would love to hear from you! Join us on [Rocket.chat](https://developer.gov.bc.ca/Steps-to-join-Rocket.Chat) now, we will be waiting for you at the [Mines Digital Trust](https://go.rocket.chat/invite?host=chat.developer.gov.bc.ca&path=invite%2FcS7ArW) channel. 👍
