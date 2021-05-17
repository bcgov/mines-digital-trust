# Business to Business Credential Manager

A fork from the [Business Partner Agent](https://github.com/hyperledger-labs/business-partner-agent).

The **Business to Business Credential Manager (BBCM)** is software run by an organization for issuing, holding, and verifying digital trust credentials. Powered by [Hyperledger](https://www.hyperledger.org/), with BBCM organizations can share and receive proofs that are secure and verifiable. Want to become an early adopter? The videos below can help you learn more about it:

- [BBCM Ep1 - Introduction](https://app.animaker.com/animo/6K3qDbzPA1DmDkAE/)
- [BBCM Ep2 - Use Cases](https://app.animaker.com/animo/BwR72vxT4hwUntX5/)
- [Product Demos](https://www.youtube.com/playlist?list=PLGAON5KTnv0EAicXGX4V3q7zNkP9p1xYF)

## **Who can use it?**

Any organization who wants to participate in the digital trust ecosystem by issuing, holding, and verifying digital trust credentials can use the Business to Business Credential Manager. For example, government, company, third-party, etc.

## **How does it work?**

To understand the big picture, let's start with the key concepts.

- **Decentralized Identifier (DID)**: Defined by the W3C DID specification, a DID
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
  2. The *Issuer* organization and *Holder* organization make a connection via their Business to Business Credential Managers.
  3. The *Issuer* organization issues a verifiable credential following the credential definition created from the schema to the *Holder* organization.
  4. The *Holder* organization receives the verifiable credential and stores it in its wallet.
- **Verifying Credentials**
  1. The *Verifier* organization imports or creates  a template for the proof request it wants to send.
  2. The *Verifier* organization and *Holder* organization make a connection via their Business to Business Credential Managers.
  3. The *Verifier* organization sends a proof request using the predefined proof request template to the *Holder* organization.
  4. The *Holder* organization receives the proof request and presents the proof by disclosing chosen verifiable credentials and/or chosen attribute values of the verifiable credentials it holds in its wallet to the *Verifier* organization.

## User Interface

The UI mock-ups are under ongoing updates, you can use the following links to access the latest contents. The links are suggested to be opened in new tabs:

- [UI Prototype - Generic Key Screens](https://xd.adobe.com/view/e2ac3e6e-113d-4d77-a71d-c2b19526e9cc-b7ff/?fullscreen)
- [Mocked-up User Workflow - Send connection request](https://xd.adobe.com/view/a515d7d3-89c2-4f8a-a67a-6f75a432fc45-f046/?fullscreen)
- [Mocked-up User Workflow - Generate QR code](https://xd.adobe.com/view/abf970f7-97b0-4730-8286-a7f52ade2496-feaa/?fullscreen)
- [Mocked-up User Workflow - Import schema for issuing credential](https://xd.adobe.com/view/fa5ffe50-2adb-46a9-9896-df66fd5cf377-af0c/?fullscreen)
- [Mocked-up User Workflow - Create schema for issuing credential](https://xd.adobe.com/view/9b9d7c70-dddd-480d-bc73-8e387b83f5e7-cece/?fullscreen)
- [Mocked-up User Workflow - Issue credential](https://xd.adobe.com/view/f9886778-d782-4800-bd9d-1775278ee448-acdb/?fullscreen)
- [Mocked-up User Workflow - Create template for sending proof request](https://xd.adobe.com/view/f3862e48-80f9-44f3-896b-fc9b5f8614f4-a6d5/?fullscreen)
- [Mocked-up User Workflow - Send proof request using template](https://xd.adobe.com/view/735c0c52-0479-4028-be1d-59749d11307c-260f/?fullscreen)
- [Mocked-up User Workflow - Respond proof request with selective proof presentation](https://xd.adobe.com/view/0206ad44-9507-46f6-9f6e-156591882b53-5755/?fullscreen)

### Terms & Usage Descriptions in the UI

![image](https://user-images.githubusercontent.com/58751681/117503092-55a5f880-af35-11eb-995f-48b4ac11e8b4.png)

- **Dashboard** - This is the page where you can find the Decentralized Identifier (DID) of your organization and view the statistics such as:
  - **Number of Credentials You Hold** - This refers to the verifiable credentials issued to your organization by your business connections. Clicking on it will link you to the Wallet page.
  - **Number of Credentials You Issued** - This refers to the verifiable credentials your organization issued to your business connections. Clicking on it will link you to the Credential Management page.
  - **Number of Sent Proof Requests** - This refers to the proof requests your organization sent to your  business connections. Clicking on it will link you to the "Sent proof request" section on the Proof Requests page.
  - **Number of Received Proof Requests** - This refers to the proof requests your organization received from your business connections. Clicking on it will link you to the "Received proof request" section on the Proof Requests page.
  - **Number of Business Connections** - Organizations are required to be "connected" via their Business to Business Credential Managers before they can issue verifiable credential or send proof request to each other. Organizations which have established such connections are referred to as "business connections" with each other. Clicking on it will link you to the Connections page.
  - **Number of New Notifications** - There are different types of notifications you can receive and act on. For example, New Connection Requests, New Credential Invitations, Credential Issuance Requests, Proof Requests, etc. Clicking on it will link you to the Notifications page.

![image](https://user-images.githubusercontent.com/58751681/118567513-c796f280-b72a-11eb-99fe-95d7ba2fb685.png)

- **Profile**: This is the page where you can view the information of your organization which is set to be visible to your business partners. It includes:
  - Administrative information (e.g. Name, Address, Email, etc.) of your organization which can be edited on the Settings page
  - List of verifiable credentials your organization holds which are set to be visible to your business partners
  - List of types of verifiable credentials your organization can issue to your business partners

![image](https://user-images.githubusercontent.com/58751681/118567544-d41b4b00-b72a-11eb-8699-5eab23e905de.png)

- **Wallet** - This is the page where you can view a list of verifiable credentials issued to your organization by your business connections and set the visibility of them on the Profile page. You can view detailed information of a certain verifiable credential including: issuer, issuance date, attribute names and values, etc. by clicking on it.

![image](https://user-images.githubusercontent.com/58751681/118567603-ef865600-b72a-11eb-8bd9-860816e964d0.png)

- **Credential Management** - This is the page where you issue verifiable credentials to your business connections and track issued verifiable credentials.
  - **Credential Schema** - 
  - **Credential Definition** - 

![image](https://user-images.githubusercontent.com/58751681/118567634-fa40eb00-b72a-11eb-93d3-2268b555e47a.png)

- **Proof Requests** - This is the page where you send proof requests to your business connections, and track sent proof requests; view received proof requests from your business connections, and present proofs in response to received proof requests.
  - **Proof Request Template** - 

![image](https://user-images.githubusercontent.com/58751681/118567650-0331bc80-b72b-11eb-94b1-2105de28ef16.png)

- **Connections** - This is the page where you can view and manage a list of organizations and/or individuals which your organization has established business connections with. You can view the Profile page and additional information of a certain organization business connection by clicking on it. You can also send connection request to a certain organization via DID lookup or generate QR code as a connection invitation.
  - **Network** - 
  - **Connection Request** - 
  - **Connection Invitation QR Code** - 

![image](https://user-images.githubusercontent.com/58751681/118567672-10e74200-b72b-11eb-8172-ef92406a4192.png)

- **Notifications** - This is the page where you can view and act on different types of notifications including:
  - **New Connection Requests** - 
  - **New Credential Invitations** - 
  - **Credential Issuance Requests** - 
  - **Proof Requests** - 

## How to Contribute

Collaborations are highly appreciated, please follow the [guidelines](./CONTRIBUTING.md) if you are interested in contributing. (Please note that this project is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.)

We would love to hear from you! Join us on [Rocket.chat](https://developer.gov.bc.ca/Steps-to-join-Rocket.Chat) now, we will be waiting for you at the [Mines Digital Trust](https://go.rocket.chat/invite?host=chat.developer.gov.bc.ca&path=invite%2FcS7ArW) channel. 👍
