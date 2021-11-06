---
layout: beta

name: User Guide
title: User Guide
order: 2
---
So now you probably have granted [access](access.html) to the **Enterprise Wallet Proof of Concept (PoC)**. Not sure where to start? Don't worry, you will be equipped with necessary knowledge by learning some key concepts from the [Knowledge Center](knowledge.html). This guide below will also help you explore the features.

#### How to...?

- How to set up the **Your Organization** page?
  - The Your Organization page contains public information (e.g. Organization Legal Name, Organization Alternate Name, Address, etc.) of your organization.
  - You can view and edit the information by navigating to the Your Organization page through the left vertical menu.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-set-up-profile.png" alt="screen-set-up-profile" title="screen-set-up-profile">
</div>

- How to **connect with another organization or individual**?
  - To perform transactions (e.g. issue verifiable credentials, send proof requests, etc.), you need to first be connected with the other organization or individual (i.e. become secure connections with each other).
  - You can view a list of your existing  secure connections or initiate a new connection request/invitation by navigating to the Secure Connections page through the left vertical menu.
  - To send a connection request, you start with looking up the other organization by its DID.
  - You can also generate a QR code as a connection invitation, and then send it externally (e.g. email, etc.) to the other organization.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-establish-connection.png" alt="screen-establish-connection" title="screen-establish-connection">
</div>

- How to **get prepared for issuing verifiable credentials**?
  - A credential schema and a credential definition are required for issuing verifiable credentials.
  - You can create them by navigating to the Settings page through the left vertical menu.
  - Make sure the "Expert Mode" is on.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-create-schema.png" alt="screen-create-schema" title="screen-create-schema">
</div>

- How to **issue a verifiable credential**?
  - Once you have the credential schema and credential definition in place (please see the above question if not), you can start issuing the verifiable credential on either the Credential Issuance page or the Secure Connections page.
  - If you go to the Credential Issuance page, select the connection you want to issue to first, then select the credential schema, then fill in the attribute values, and you are ready to hit the "Issue Credential" button.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-issue-credential-1.png" alt="screen-issue-credential" title="screen-issue-credential">
</div>
  - If you go to the Secure Connections page, select the connection you want to issue to first, then on its details page, issue the credential by selecting the credential schema, then fill in the attribute values.
<div class="text-center mb-5">
    <img class="img-fluid" src="{{ site.baseurl }}/assets/images/screen-issue-credential-2.png" alt="screen-issue-credential" title="screen-issue-credential">
</div>
