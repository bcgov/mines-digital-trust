---
layout: solutions
name: PoC

title: Enterprise Wallet Proof of Concept
order: 1
description: The Enterprise Wallet Proof of Concept (PoC) is software run by an organization for issuing, holding, and verifying digital trust credentials. With the Enterprise Wallet PoC, which is Powered by the Hyperledger Labs Business Partner Agent project, organizations can share and receive proofs that are secure and verifiable.
---
#### **Useful Links**

- [Repo: Business Partner Agent (BPA)](https://github.com/hyperledger-labs/business-partner-agent)
- [Repo: Enterprise Wallet Proof of Concept (PoC)](https://github.com/bcgov/b2b-credential-manager)
- [Playlist: Digital Trust Ecosystem](https://youtube.com/playlist?list=PL9CV_8JBQHiooHv05idOTrR2eBAJM89LX)

#### **Who can use it?**

Any organization who wants to participate in the digital trust ecosystem by issuing, holding, and verifying digital trust credentials can use the Enterprise Wallet PoC. For example, government, company, third-party, etc.

#### **How does it work?**

To understand the big picture, let's start with the key concepts.

- **Decentralized Identifier (DID)**: Defined by the [W3C DID specification](https://www.w3.org/TR/did-core/), a DID
  - Is globally unique
  - Can identify any subject (e.g. an organization, person, credential, transaction, etc.)
  - Is associated with exactly one subject

- **Verifiable Credential**: Similar to the driver's license you hold in your wallet, which you can use to prove your identity to a police officer, a company can be issued a registration credential from a trusted source like BC Registries. The received credential is verified. What makes a credential "verifiable"? Others can request that you present a proof to them that your credential is verified. The proof that you present to them is verifiable by the verifier who can do the verification without having to go back a ask the credential issuer. The items that can be verified include the following:
  - Can validate the issuer and holder of a credential
  - Can confirm the credential is not revoked
  - Can prove the credential has not changed

- **Wallet**: Verifiable credentials can be stored in a digital wallet. In many ways it is just like your physical one. This is where you store your organization's information that you will use to prove to other organizations that you hold a certain credential.
  
- **Proof Request**: A proof request is the message sent by the relying party to the holder describing the verifiable attributes and appropriate conditions (e.g. predicates, issuer of attributes, schema of the credentials used, etc.) that the holder needs to satisfy.

Now let's see some generic use cases.

- **Issuing and Holding a Verifiable Credential**
  1. The *Issuer* organization imports or creates  a schema for the type of verifiable credential it wants to issue.
  2. The *Issuer* organization and *Holder* organization make a connection via their enterprise wallets.
  3. The *Issuer* organization issues a verifiable credential following the credential definition created from the schema to the *Holder* organization.
  4. The *Holder* organization receives the verifiable credential and stores it in its wallet.
- **Verifying Credentials**
  1. The *Verifier* organization imports or creates  a template for the proof request it wants to send.
  2. The *Verifier* organization and *Holder* organization make a connection via their enterprise wallets.
  3. The *Verifier* organization sends a proof request using the predefined proof request template to the *Holder* organization.
  4. The *Holder* organization receives the proof request and presents the proof by disclosing chosen verifiable credentials and/or chosen attribute values of the verifiable credentials it holds in its wallet to the *Verifier* organization.

#### **Why use it?**
Please refer to the [Features](https://github.com/bcgov/mines-digital-trust/wiki/Features) list to learn about existing features and offered value to users.

#### **PoC Outcome**
The Business Partner Agent has successfully proven the concept that a digital trust ecosystem can be established upon the foundations of interoperability and open-source technology.

In 2022, BC Government Digital Trust teams will work towards a multi-tenanted solution that can be run providing enterprise wallet capabilities for each organizational unit desiring to issue, hold, and/or verify credentials.
