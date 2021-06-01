---
layout: onboarding

name: Issue credentials to OrgBook BC
title: Issue credentials to OrgBook BC
order: 1
---
#### **Step-by-Step Overview**
- **Step 1: Decide what data to issue**
  - The surprising first step in becoming an issuer is that you may need to know your own organization, and specifically its business processes, even better. Starting questions are:
    - What data “should” be in OrgBook BC?
    - What specific changes to your data should cause an update to OrgBook BC?
  - You’ll likely already have your data online, such as in a database. However, if it’s not online, that’s the first step you’ll need to take before becoming an issuer. It will not be practical (nor desirable) to manually enter and update the VCs.
  - Next, you’ll need to be more specific about what will be in OrgBook BC, and when it’s ready for OrgBook BC. For example:
    - When is a change to your data ready to show to the outside world?
    - Is it after certain approval processes?
    - Does some data need to be abstracted up or grouped in some way, in order to make it more “public friendly”?
    - What data could be added to OrgBook BC, but has little or no public value and could therefore be omitted?
    - Are there any privacy issues that must be resolved before some data can be used?
  - Diagrams of data flows and approval processes within your organization may help you decide exactly how and when your OrgBook BC issuer agent should be processing data.
  - Once you know what data is to be shared, it will need to be very clearly specified. For example:
    - What is the size and type of each piece of data you wish to have in OrgBook BC?
    - Does it have limits?
    - Where exactly is it stored right now — how can the issuer agent get access to it?
  - *For Step 1, the credential issuer has an online database of permits issued to BC organizations. They decide that OrgBook BC should know: (a) whether a BC organization has been issued a permit, (b) the permit number, (c) the permit type, (d) the date it was issued, (e) the scope of the permit, and (b) the permit’s expiry date. They decide that an internal approval code for the permit adds little value to OrgBook BC, so will not include that data. They also decide that their credential issuer agent should watch its main database for when a new permit is approved, extended, or revoked, and update OrgBook BC accordingly.*

- **Step 2: Get approval from BC Registries**
  - BC Registries and Online Services, a branch within Service BC and part of the Ministry of Citizens’ Services, are the business owners of OrgBook BC. The core information in OrgBook BC is the company registration data, which is managed by BC Registries and Online Services. The registration data is what the various program VCs are issued against. BC Registries and Online Services will need to approve your project and onboarding plan before you can be an OrgBook BC issuer on the live system.
  - Please reach out to BC Registries and Online Services at BCRegistries@gov.bc.ca, and a discovery meeting will be coordinated with your program. In most cases, the onboarding process will be smooth and simple.
  - *For Step 2, the credential issuer completes an intake process with BC Registries and Online Services where they present the data they wish to issue to OrgBook BC, and why, as well as their plans for keeping it up-to-date. BC Registries and Online Services gives permission to the credential issuer to issue their data onto the live system.*

- **Step 3: Test the OrgBook BC issuer technology**
  - This [Getting Started](https://github.com/bcgov/aries-vcr-issuer-controller/blob/master/GettingStartedTutorial.md) tutorial will give your tech teams a starting point for the onboarding process. However, the general overview is:
    - Install and test the OrgBook BC “starter kit” issuer on a single computer
    - Use the starter kit to learn about creating and issuing VCs
    - Connect your issuer to your database that holds the information you wish to issue, and ensure the issuer gets the right data from it, at the right time
    - Connect your issuer to the OrgBook BC “dev environment”, and learn about the new processes and steps involved
    - Prepare a deployment to the OrgBook BC “test environment”, and liaise with the OrgBook BC team to ensure your issuer is submitting the right data
    - Do final checks before launch on the OrgBook BC “production environment”, the live service
  - *For Step 3, the credential issuer’s technical team download, install and test the OrgBook BC “starter kit” issuer, and learn about creating and issuing VCs. They identify some short online VC training courses for key team members to better understand the technology. After adapting the starter kit to their needs, they then contact the OrgBook BC team to let them know about their plans, and start testing how they publish and revoke credentials.*

- **Step 4: Prepare for going live**
  - You’ll need a few parts aligned to be ready for launch:
    - The OrgBook BC team will need to see that your issuer is issuing the right credentials on the test environment, at the right time, and in the right format, so they can approve your ability to issue to the live OrgBook BC system
    - BC Registries approval will need to have been received
    - Ideally, if you are using the API (a software service) to integrate OrgBook BC capabilities into your website or other service for launch, it should be tested and ready, although this can happen after launch.
  - With all these components in place, and if all teams are happy, you are good to go!
  - *For Step 4, the credential issuer has some back-and-forth with the OrgBook BC team as they resolve some issues with issuing to the dev environment. The credential issuer also runs some tests to ensure their issuer agent is getting the right information from their database, and that it’s triggering an update to OrgBook BC at the right time. With all this complete, the OrgBook BC team reviews the deployment to the test environment, and launch checks are made to ensure the process is working before a deployment to the live environment.*

- **Step 5: Communicate your changes**
  - Congratulations! Your VCs are now in OrgBook BC. What’s next?
    - Communicate the new approach to your teams and partners, so they know what’s happening, where they can access this new information source, and who to contact if they have questions
    - Update your website and other public materials so that citizens and other consumers of your information now use OrgBook BC to find your data
    - Integrate OrgBook BC into your business processes, so that (for example) you update your OrgBook BC agent if something changes with how and when you issue credentials
    - If you didn’t integrate OrgBook BC data into your website before, consider using the API to provide a search facility for the data on your website, simplifying how people can find the information they desire.
  - *For Step 5, the credential issuer holds a meeting with support teams to explain the new OrgBook BC process and website, and emails everyone the OrgBook BC link so they know where to direct most information requests from now on. An extra governance step is also added to the permit issuing processes, to ensure that the tech team is notified about any changes to permit issuing so they can reflect those changes in the OrgBook BC issuer agent.*

Please [connect with OrgBook BC](https://www.orgbook.gov.bc.ca/en/connect) to start the process.
