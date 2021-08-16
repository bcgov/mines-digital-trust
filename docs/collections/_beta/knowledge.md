---
layout: beta

name: Knowledge Center
title: Knowledge Center
order: 3
---
Want to [become an early adoptor](access.html) of the Business Partner Agent (BPA)? This page will equip you with necessary knowledge of [using](guide.html) it.

#### What is...?
- What is a [**Decentralized Identifier (DID)**](https://www.w3.org/TR/vc-data-model/#dfn-decentralized-identifiers)?
  -  DIDs are a type of globally unique and persistent identifiers. They create a secure connection for data exchange between parties and their decentralized nature makes credentials always available for verification.
  -  For example, each BPA has a DID representing the organization who runs it, which can be exchanged to connect with other organizations running BPAs.

- What is a [**Verifiable Credential (VC)**](https://www.w3.org/TR/vc-data-model/#what-is-a-verifiable-credential)?
  -  The physical credentials we use in our daily lives – like ID Card, Driver’s license, Health Insurance Card or even a University Diploma – rarely have a counterpart in the digital world. How could a digital credential, a digital asset, be as trustworthy as the physical ID Card that your Government issued to you?
  -  Verifiable Credentials, in essence, allow for the digital watermarking of claims data through a combination of public key cryptography and privacy-preserving techniques to prevent correlation. Not only can physical credentials safely be turned digital, holders of such credentials can selectively disclose specific information from this credential without exposing the actual data (imagine proving you are above the age of 21 without having to show your ID card), where third-parties are instantly able to verify this data without having to call upon the issuer.

- What is a [**Credential Schema**](https://www.w3.org/TR/vc-data-model/#data-schemas)?
  - Per the W3C, “The Credential Schema is a document that is used to guarantee the structure, and by extension the semantics, of the set of claims comprising a Verifiable Credential. A shared Credential Schema allows all parties to reference data in a known way.
  - To put it more simply, a Schema is a template, outlining the verified data you can issue or verify from your users.
  - For example, a Credential Schema for a University Diploma may include Name of Student, Degree Name, Date of Completion, Grade, etc. The University would use this schema to issue the Diploma Credential. A verifier, like an employer, would use the schema if they want to verify if the job candidate has a valid University diploma and what degree they did.

- What is a **Credential Definition**?
  - A Credential Definition is an instance of the schema on which it is based, plus the attribute-specific public verification keys that are bound to the private signing keys of the individual issuer.
  
- What is a [**Proof**](https://www.w3.org/TR/vc-data-model/#proofs-signatures)?
  - A Proof is data about the holder that allows others to verify the source of the data (i.e the issuer), check that the data belongs to the holder (and only the holder), that the data has not been tampered with, and finally, that the data has not been revoked by the issuer.
