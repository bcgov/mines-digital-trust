---
layout: service
name: GUIDE

title: User Guide
description: The Business Partner Agent (BPA) is software run by an organization for issuing, holding, and/or verifying digital trust credentials. This guide provides users required knowledge for getting started.
---
So now you have accessed to your organization's BPA (please check the [Get Access](access.html) page if not), not sure where to start? Don't worry, you will be equipped with necessary knowledge by reading the sections below. The "What is...?" section will intruduce you the key concepts and the "How to...?" section will help you explore the key features. There are also really good readings recommended under the "Useful Links" below.

#### Useful Links
- [The Ultimate Beginners Guide - Verifiable Credentials (VCs)](https://tykn.tech/verifiable-credentials/)
- [The Ultimate Beginners Guide - Decentralized Identifiers (DIDs)](https://tykn.tech/decentralized-identifiers-dids/)
- [The Ultimate Beginners Guide - Self-Sovereign Identity (SSI)](https://tykn.tech/self-sovereign-identity/)

#### What is...?
- What is a **Decentralized Identifier (DID)**?
  -  DIDs are a type of globally unique and persistent identifiers. They create a secure connection for data exchange between parties and their decentralized nature makes credentials always available for verification.
  -  For example, each BPA has a DID representing the organization who runs it, which can be exchanged to connect with other organizations running BPAs.

- What is a **Verifiable Credential (VC)**?
  -  The physical credentials we use in our daily lives – like ID Card, Driver’s license, Health Insurance Card or even a University Diploma – rarely have a counterpart in the digital world. How could a digital credential, a digital asset, be as trustworthy as the physical ID Card that your Government issued to you?
  -  Verifiable Credentials, in essence, allow for the digital watermarking of claims data through a combination of public key cryptography and privacy-preserving techniques to prevent correlation. Not only can physical credentials safely be turned digital, holders of such credentials can selectively disclose specific information from this credential without exposing the actual data (imagine proving you are above the age of 21 without having to show your ID card), where third-parties are instantly able to verify this data without having to call upon the issuer.
  -  [Video: What are Verifiable Credentials?](https://youtu.be/hjfiK5cBDPM)

- What is a **Credential Schema**?
  - Per the W3C, “The Credential Schema is a document that is used to guarantee the structure, and by extension the semantics, of the set of claims comprising a Verifiable Credential. A shared Credential Schema allows all parties to reference data in a known way.
  - To put it more simply, a Schema is a template, outlining the verified data you can issue or verify from your users.
  - For example, a Credential Schema for a University Diploma may include Name of Student, Degree Name, Date of Completion, Grade, etc. The University would use this schema to issue the Diploma Credential. A verifier, like an employer, would use the schema if they want to verify if the job candidate has a valid University diploma and what degree they did.

- What is a **Credential Definition**?
  - A Credential Definition is an instance of the schema on which it is based, plus the attribute-specific public verification keys that are bound to the private signing keys of the individual issuer.
  
- What is a **Proof**?
  - A Proof is data about the holder that allows others to verify the source of the data (i.e the issuer), check that the data belongs to the holder (and only the holder), that the data has not been tampered with, and finally, that the data has not been revoked by the issuer.

#### How to...?

- How to set up the **Public Profile** for your organization?
  - The Public Profile contains information (e.g. Company Legal Name, Company Alternate Name, Address, etc.) of your organization and is visible to your business partners/connections.
  - You can view and edit the information by navigating to the "Public Profile" page through the left vertical menu.

- How to **connect with another organization or individual**?
  - To perform transactions (e.g. issue verifiable credentials, send proof requests, etc.), you need to first be connected with the other organization or individual (i.e. become business partners/connections with each other).
  - You can view a list of your existing business partners/connections or initiate a new connection request/invitation by navigating to the "Business Partners" page through the left vertical menu.
  - To send a connection request, you start with looking up the other organization by its DID.
  - You can also generate a QR code as a connection invitation, and then send it externally (e.g. email, etc.) to the other organization.

- How to **get prepared for issuing verifiable credentials**?
  - A credential schema and a credential definition are required for issuing verifiable credentials.
  - You can create them by navigating to the "Credential Management" page through the left vertical menu.

- How to **issue a verifiable credential**?**
  - Once you have the credential schema and credential definition in place (please see the above question if not), you can start issuing the verifiable credential on either the "Credential Management" page or the "Business Partners" page.
  - If you go to the "Credential Management" page, select the business partner/connection you want to issue to first, then select the credential schema, then fill in the attribute values, and you are ready to hit the "Issue Credential" button.
  - If you go to the "Business Partners" page, select the business partner/connection you want to issue to first, then on its details page, issue the credential by selecting the credential schema, then fill in the attribute values.

**How to get prepared for sending proof requests?**

**How to send a proof request?**
