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
- **Actors**
  - *Director* - Refers to a director of a business (company/organization) or the director's personal digital wallet.
  - *Business* - Refers to a business (company/organization) or its Business Partner Agent.
  - *Corporate Registrar* - Refers to BC Corporate Registry and its Business Partner Agent.
- **Step 1: Director Issued Personal Credential from Corporate Registrar**
  - *Director* presents personal id and business documents to *Corporate Registrar* in person.
  - *Corporate Registrar* inspects the personal id and the business documents, determines that the *Director* is who they say they are and indeed a director for the *Business*.
  - *Corporate Registrar* creates invitation to *Director* (generates a QR code).
  - *Director* opens their personal digital wallet, scans the QR code, and accepts invitation.
  - *Corporate Registrar* makes the connection with *Director* active.
  - *Corporate Registrar* and *Director* are now connected with each other. *Corporate Registrar* can issue credential to *Director*.
  - *Corporate Registrar* issues **Business Relationship credential** to *Director*, indicating that they are a director of the *Business*. Included in that credential is a hashcode or key (could be the credential id) that *Corporate Registrar* tracks.
  - *Director* receives and accepts the **Business Relationship credential**.
  - *Director* has a verifiable credential issued by *Corporate Registrar* in their personal digital wallet relating them to the *Business*.
- **Step 2: Director sets up a Business Wallet**
  - *Director* sets up a [Business Partner Agent](https://github.com/hyperledger-labs/business-partner-agent) for the *Business*, and registers it on the same ledger as *Corporate Registrar*.
  - *Director* creates a self-attested **Business Registration credential**.
  - *Business* creates invitation to *Director* (generates a QR code).
  - *Director* opens their personal digital wallet, scans the QR code, and accepts invitation.
  - *Business* makes the connection with *Director* active.
  - *Business* requests proof of **Business Relationship credential** from *Director*.
  - *Director* sees the proof request from *Business* in their personal digital wallet, selects their **Business Relationship credential**, and sends the proof which includes the hashcode/key/id that pairs the *Director* to the *Business* in *Corporate Registrar*.
  - *Business* receives the proof and knows that *Director* is indeed a director for the *Business*, sets the partner state to active and tags partner as Individual and Director.
  - *Business* updates their self-attested **Business Registration credential**.
- **Step 3: Business wants their Credential from Corporate Registrar**
  - *Business* initiates connection with *Corporate Registrar*.
  - *Corporate Registrar* accepts invitation and makes the connection with *Business* active.
  - *Business* sends a presentation proposal of their self-attested **Business Registration credential** which includes the hashcode/key/id from the *Director*'s proof of **Business Relationship credential** to *Corporate Registrar*.
  - *Corporate Registrar* inspects the proposal, matches the hashcode/key/id from the *Business*'s self-attested **Business Registration credential** and the one they track.
  - *Corporate Registrar* issues **Business Registration credential** to *Business*.
  - *Business* receives and accepts the **Business Registration credential**.
  - *Business* has a verifiable credential in their wallet issued by *Corporate Registrar*.
