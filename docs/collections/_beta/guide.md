---
layout: beta

name: User Guide
title: User Guide
order: 2
---
So now you probably have granted [access](access.html) to the **Enterprise Wallet Proof of Concept (PoC)**. Not sure where to start? Don't worry, you will be equipped with necessary knowledge by learning some key concepts from the [Knowledge Center](knowledge.html). The guide below will also help you explore the key features by informing where and how to accomplish certain tasks.

#### How to...?

- How to set up the **Your Organization** page?
  - The Your Organization page contains public information (e.g. Organization Legal Name, Organization Alternate Name, Address, etc.) of your organization.
  - You can view and edit the information by navigating to the Your Organization page through the left vertical menu.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-set-up-profile.png" alt="screen-set-up-profile" title="screen-set-up-profile">
</div>

- How to **connect with another organization or individual**?
  - To perform transactions (e.g. issue verifiable credentials, send proof requests, etc.), you need to first be connected with the other organization or individual, i.e. become secure connections with each other.
  - You can view a list of your existing  secure connections, or initiate a new connection request or invitation by navigating to the Secure Connections page through the left vertical menu.
  - To send a connection request, you start with looking up the other organization by its DID. To do so, you click on the plus button on the page and follow the instructions from there.
  - You can also generate a QR code / a equivalent URL as a connection invitation, and then send it externally (e.g. email, etc.) to the other organization or individual. To do so, you click on the QR code button on the page and follow the instructions from there.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-establish-connection.png" alt="screen-establish-connection" title="screen-establish-connection">
</div>

- How to **get prepared for issuing verifiable credentials**?
  - Schema and credential definition are required for issuing verifiable credentials.
  - You can import or create them by navigating to the Settings page through the left vertical menu.
  - Make sure the "Expert Mode" is on first.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-create-schema.png" alt="screen-create-schema" title="screen-create-schema">
</div>

- How to **issue a verifiable credential**?
  - Once you have the schema and credential definition in place (please see the above question if not), you can start issuing the verifiable credential on either the Credential Issuance page or the Secure Connections page.
  - If you go to the Credential Issuance page, select the connection you want to issue the credential to first, then select the template, i.e. the credential definition, then fill in the attribute values following the instructions from there, and you are ready to hit the "Issue Credential" button.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-issue-credential-1.png" alt="screen-issue-credential" title="screen-issue-credential">
</div>
  - If you go to the Secure Connections page, select the connection you want to issue the credential to first, then on its details page, click on the "Issue Credential" button and follow the instructions from there.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-issue-credential-2.png" alt="screen-issue-credential" title="screen-issue-credential">
</div>

- How to **get prepared for sending proof requests**?
  - Proof template is required for sending proof requests.
  - You can create and manage it by navigating to the Proof Templates page through the left vertical menu.
  - Click on the "Create Proof Template" button and define data to be requested by selecting credential(s) and data field(s), then setting restrictions if needed from there.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-create-proof-template.png" alt="screen-create-proof-template" title="screen-create-proof-template">
</div>

- How to **send a proof request**?
  - Once you have the proof request template in place (please see the above question if not), you can start sending the proof request on the Secure Connections page.
  - Select the connection you want to send the request to first, then on its details page, click on the "Request Proof" button and follow the instructions from there.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-send-proof-request.png" alt="screen-send-proof-request" title="screen-send-proof-request">
</div>

- How to **chat with a secure connection**?
  - You can send and receive instant messages securely with your connections.
  - Click on the message icon in the bottom right cornor, then search for and select a secure connection to initiate the chat.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-message.png" alt="screen-message" title="screen-message">
</div>
