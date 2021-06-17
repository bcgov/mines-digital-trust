---
layout: onboarding

name:  Run your own Digital Wallet
title:  Run your own Digital Wallet
order: 2
---
#### **For whom**
If your organization is external to the BC Government and needs to issue, hold, and/or verify verifiable credentials, this option is suitable for you.

As of today, running your own copy of the [Business Partner Agent](https://github.com/hyperledger-labs/business-partner-agent) is the only available option.

In the near future, your organization would run an instance of the [Business to Business Credential Manager](https://github.com/bcgov/b2b-credential-manager) instead, our team has been working diligently towards enabling it.

#### **Step-by-Step Overview**
- **Step 1: Director Issued Personal Credential from Corporate Registrar**
  - IND to REG: in person, presents personal id and Business Incorporation papers.
  - REG inspects the personal id credential and the Business Incorporation papers, determines that IND is indeed a director for ABC and is who they say they are.
  - REG creates invitation to IND (generates a QR Code).
  - IND opens their wallet, scans the QR Code and accepts invitation.
  - REG makes the connection to IND active and tags Partnership as needed.
  REG and IND are now connected to each other; REG can issue credential.
  - REG issues BizRel credential to IND, indicating they are a director of ABC. Included in that credential is a hashcode or key (could be the credential id) that REG tracks that indicates the IND and BIZ.
  - IND reviews and accepts the credential.
  - IND has a VC in their wallet relating them to ABC from REG.
- **Step 2: Director sets up a Business Wallet**
  - IND sets up a BPA for ABC, and registers it on the same ledger as REG.
  - IND creates a self attested Business Registration credentials (BizNum) with ABC Business Number.
  ABC wallet is empty.
  - ABC creates invitation to IND, generates a QR code.
  - IND opens their wallet, scans QR Code and accepts invitation.
  - ABC sets connection active, partner is in unknown state.
  - ABC requests proof of BizRel from IND (where business number = ABCs business number).
  - IND sees proof request from ABC in phone, selects their ABC Biz Rel credential and sends the Proof (which includes the hashcode/key/id that pairs the IND to ABC in REG).
  - ABC receives the proof and knows that IND is indeed a director/officer of ABC, sets the partner state to active and tags partner as Individual and Director.
  - ABC updates their self attested Business Registration credentials (BizNum).
- **Step 3: Business wants their Credential from Corporate Registrar**
  - ABC initiates connection with REG.
  - REG accepts invitation and activates connect, but partnership is inactive/unknown.
  - ABC sends a Presentation Proposal of their self-attested Business Number document (contains their Business Number and the hashcode/key from the IND BizRel proof) to REG.
  - REG inspects the proposal, matches the Business Number and IND hashcode, sets partnership active and tags them for grouping/sorting/id.
  - REG issues Business Registration credentials (BizNum).
  - ABC receives Business Registration credentials.
  - ABC can put partnership with REG into a good state and tag them.
  ABC has a credential in their wallet issued from Corporate Registrar.
