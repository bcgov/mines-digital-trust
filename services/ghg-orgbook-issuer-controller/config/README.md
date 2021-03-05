# VON Issuer/Verifier Agent Configuration

This folder contains the files used to configure a VON issuer/verifier agent. If you are going to be updating a VON issuer/verifier agent, please review this documentation thoroughly, looking particularly for changes that need to be made across several of the configuration files.

## Table of Contents <!-- omit in toc -->

- [VON Issuer/Verifier Agent Configuration](#von-issuerverifier-agent-configuration)
  - [Summary: The Configuration Files](#summary-the-configuration-files)
  - [File: schemas.yml](#file-schemasyml)
  - [File: settings.yml](#file-settingsyml)
  - [File: routes.yml](#file-routesyml)
  - [File: services.yml](#file-servicesyml)

## Summary: The Configuration Files

There are (currently) four configuration files used to configure a VON issuer/verifier agent.  Each of the configuration files is a [YAML file](https://en.wikipedia.org/wiki/YAML). Although YAML makes it easy to structure data (with way fewer characters than XML or JSON), it is very important to remember when editing a YAML file that the indentations of the lines are important and must be consistent, and that the indenting must ONLY use spaces, never tab characters. When editing these files, we recommend using a text editor that has a YAML configuration and better, a YAML linter to make sure the file structure is correct.

The following is a brief summary of the purpose of each of the VON issuer/verifier agent configuration files:

- **`schemas.yml`** holds the schema attributes for the set of credentials to be issued by the agent. Based on this information, the agent can, on startup, look up on, and if necessary, publish to, the ledger the schema and credential definitions for the credentials to be issued by the agent.
- **`settings.yml`** contains a list of environment variables that must be set appropriately to allow the agent to connect to the other components of VON, specifically, the ledger being used and an instance of OrgBook. The values in the file change with each environment (e.g. local, in browser, dev, test and prod).
- **`routes.yml`** holds information that allows the agent to render a form on a web page to collect information about a credential to be issued. While not normally used in a production use case (a service likely already has data collection capabilities), the form is useful for testing purposes and for use with GreenLight.
- **`services.yml`** defines how attributes in the credentials issued by the agent should be processed by OrgBook. This includes the mapping of attributes to OrgBook search indices and the localization of strings in the UI for each credential.

The sections that follow detail the contents and usage of each file.

## File: [schemas.yml](schemas.yml)

The following is a simple `schemas.yml` file with a single credential having a single atttribute.

``` YAML
- name: my-permit.my-organization.ca
  version: '1.0.2'
  attributes:
    - corp_num
    - legal_name
```
Pretty simple!  The following are notes about the example file above and `schemas.yml` files in general.

- The entire `name` structure is repeated for each type of credential that is to be issued by the agent.
- The elements `name`, `version` and the `attributes` list (e.g. `corp_name` in the above example) correspond exactly to those same elements in a Hyperledger Indy schema. If the Indy schema structure evolves, the VON schema structure in this file will likely evolve to match.
- The sub-elements within each `attribute` (`label_en`, etc.) are used in VON,they do not flow to the Hyperledger Indy schema.
- The "_en" fields are localized (in this case for English). You can pass additional fields with different suffixes for other languages (e.g. "_fr") to enable localized presentation in OrgBook.


  On startup, the VON issuer/verifier agent reads the `schemas.yml` file and looks in its wallet for the corresponding credential definitions and schemata. If it does not find them, the agent publishes them to the ledger. 
  - **NOTE**: VON issuer/verifier agent currently assumes that the agent itself will always publish the schema to the ledger. **TO DO** Confirm this.

## File: [settings.yml](settings.yml)

Settings is a simple list of variables that must be set appropriately to run an instance of an agent that connects to specific instances of OrgBook and the ledger. Since the instance of OrgBook and the ledger vary with each environment (e.g. local, in browser, dev, test and prod), managing the contents of the file can be challenging. In an automated environment, these values are injected at deployment time.

The following is an example `settings.yml` file:

``` YAML
default:
  APPLICATION_URL_INCORP: $APPLICATION_URL/bcreg/incorporation
  APPLICATION_URL_DBA: $APPLICATION_URL/bcreg/dba
  TEMPLATE_PATH: ../templates
  TOB_API_URL: http://tob-api:8080/api/v2
  TOB_APP_URL: http://localhost:8080
  INDY_WALLET_SEED: bc_registries_dev_00000000000000
  INDY_GENESIS_URL: https://raw.githubusercontent.com/sovrin-foundation/sovrin/1.1.50-master/sovrin/pool_transactions_sandbox_genesis
  LEDGER_PROTOCOL_VERSION: "1.6"
  AUTO_REGISTER_DID: 0
```

The following describes the purpose of each element:

- `APPLICATION_URL_XXX` is the URL for each credential issued by the agent. The last two elements correspond to the path defined in the `routes.yml` file for the credential. The `$APPLICATION_URL` is the server part of the URL for the agent.
- `TEMPLATE_PATH` is the location of the web form HTML templates referenced in the `routes.yml` file.
- `TOB_API_URL` is the URL of the API for the instance of OrgBook to which the agent will issue credentials.
- `TOB_APP_URL` is the URL of the application the instance of OrgBook to which the agent will issue credentials.
  - **NOTE**: In the example above, although the same instance of OrgBook is referenced in both cases, the server section is different because of the vagaries of Docker
- `INDY_WALLET_SEED` is the seed used to generate the encryption keypair for the agent wallet. This approach is used for testing. In production, the seed is handled in a secure manner, injected at startup time from a vault.
- `INDY_GENESIS_URL` is the URL from which the genesis file for the instance of the Indy ledger that the agent is using.
- `LEDGER_PROTOCOL_VERSION` is  the protocol version of the instance of the Indy ledger that the agent is using. Must be at least 1.6.
- `AUTO_REGISTER_DID` is 1 if the agent should register the DID of the agent to the Indy ledger, 0 if not.
  - **NOTE**: In production, the Agent's DID is written to the ledger before the initial deployment of the agent. Often in testing a script is used to pre-write the DID to the ledger to mimic the production behaviour.

## File: [routes.yml](routes.yml)

The `routes.yml` file configures the web server routes for the API and the web forms template invoked by a user requesting a credential interactively, such as with GreenLight. The agent web forms are unlikely to be used in a production VON issuer/verifier agent instance, but the form is super useful for testing. The configuration drives a dynamic form (based on the claim names and attributes) so that a user can request a credential by filling out and submitting the web form.

An example of a simple `routes.yml` file is the following:

``` YAML
forms:
  my-permit:
    path: /my-organization/my-permit
    type: issue-credential
    schema_name: my-permit.my-organization.ca
    page_title: my-org-full-name Permits
    title: Application for my-permit
    template: bcgov.index.html
    description: >
      my-org-full-name issues my-permit credentials to organizations to authorize those organizations to be able to do something.

    explanation: Use the form below to apply for a my-permit for your organization.

    proof_request:
      id: greenlight_registration
      connection_id: bctob

    js_includes:
      - src: js/bc_registries.js

    fields:
      - name: corp_num
        label: Corp Num
        type: text
        required: true

      - name: permit_type
        label: Permit Type requested
        type: select
        options:
          - Limited Use Authorization
          - Unlimited Use Authorization
        required: true

    mapping:
      attributes:
        - name: permit_id
          from: helper
          source: uuid

        - name: permit_issued_date
          from: helper
          source: now_iso
```

The following are notes about the example presented above:

- There must be a structure below `forms` for each form defined in the application.
  - In general, there will be a form defined for each credential in the `schemas.yml` file. You can define multiple forms for a credential (by having a different path for each), or you could not have any form for a credential.
- `path` is the VON issuer/verifier agent web app "route" to the form.
- `type` is defined by the VON issuer/verifier agent and is currently always `issue-credential`.
- `schema-name` must match exactly the name of one of the schema in `schemas.yml`
- The `title`, `page_title`, `description` and `explanation` are fields that can be referenced in the HTML template for the web form.
- `template` is the name of a file that must exist in the folder referenced by the `TEMPLATE_PATH` value in the `settings.yml` file (described above).
  - if `js_includes` `src` is set, the value must be a file also within the `TEMPLATE_PATH` folder.
- The `proof_request`, `fields` and `mapping` section are discussed below.

As the web form loads, any `proof_request` entries referenced in this file (`routes.yml`) and defined in `services.yml` are executed and must be successful for the form to load. If a `proof_request` is referenced and the proof request fails, the form does not load and an error message is displayed. A referenced `proof_request` could fail either because no identifier is passed to the form (so no proof request to OrgBook is possible), or if the identified organization does not have the required active credential.  Any attribute in the form's credential that has the same name as a claim in a prerequisite proof request is pre-populated with the value of the proven claim.


`fields` is a list of the attibutes that are to be listed on the web form with a `label` and a `type` that defines how the data will be collected (for example, what widget will be used for the field). The `required` defines if the field must be filled in to submit the credential. The current list of options are the following:

- `text` - a text field
- `date` - a date field, with calendar support.
- `select` - a dropdown list of enumerated values driven by the `options` list.
- `address` - a special, multi-field widget for entering a Canadian address that includes auto-complete (using the Canada Post auto-complete API).
  - An example of the use of the `address` field type can be seen [here in GreenLight](https://greenlight.orgbook.gov.bc.ca/bcreg/incorporation?credential_ids=&schema_name=registration.greenlight&schema_version=1.0.0&issuer_did=6qnvgJtqwK44D8LFYnV5Yf) - the fields from the "Mailing Address" label down to "Postal Code" and "Country" fields.

`mappings` is a list of attributes that are auto-populated by one of a number of helpers. The current set of helper functions can be found by looking at [this code from the VON-X repo (master branch)](https://github.com/PSPC-SPAC-buyandsell/von-x/blob/master/vonx/web/helpers.py).

All fields in the credential (or at least all required fields) must be in either the `fields` list or the `mappings` list, even if the field has the same name as a proven claim.

## File: [services.yml](services.yml)

`services.yml` provides configuration information for OrgBook about the agent's issuer and the credentials. OrgBook has functionality related to its role as a "community wallet" and searchable web service, but has been designed to be agnostic about the credentials it receives. The credential configuration data in `services.yml` provides information from the issuer that tells OrgBook map instances of issued credentials into OrgBook concepts. That's a little abstract, so we'll provide some background information in this section on the features of OrgBook.

The following lists a number of features of OrgBook that require information from credential issuers in order to work:

- OrgBook provides several search capabilities, including names, addresses/locations, credential types and dates. 
  - `services.yml` provides information about what attributes should be added to the different search indices (for example, what credential attribute is a "name" that should be searchable, and so on).
- OrgBook has the concept of a "subject entity"&mdash; the entity  that is the subject of a credential (for example, an incorporated organization, a sole proprietorship, a professional, etc.). Further, OrgBook has the concept that all credentials issued to an instance of the OrgBook include an attribute that links that credential to its subject entity.
  - `services.yml` informs OrgBook what attribute in an issued credential is its subject entity ID.
- OrgBook has a user interface that can be customized by OrgBook instance to display information about credentials and entities in user-friendly language based on attributes pulled from credentials. For example, an OrgBook instance might display a label "Credential Effective Date" for all credentials and must know what attribute holds that value for each credential.
  - `services.yml` maps credential attributes to OrgBook instance-specific data elements for presentation in the user interface for each OrgBook instance.
  - **NOTE**: In addition, `schemas.yml` provides localized information about attributes that are also presented in the user interface.
- OrgBook has the concept of a credential "cardinality" based on a unique key derived from one or more attributes. When a credential is received, OrgBook marks the credential as new or as a replacement for an existing credential (marking that one as inactive) based on the data in the cardinality attributes.
  - `services.yml` defines the cardinality of each credential the agent issues. 
  - OrgBook uses the cardinality to present a timeline of each credential set&mdash; credentials issued with the same data values in the cardinality attributes.

The following is an example of a basic `services.yml` file, broken into sections. Notes about the content follows the section of the example:

``` YAML
# Documentation: https://github.com/bcgov/von-agent-template/tree/master/von-x-agent/config

issuers:
  my-organization:
    name: my-org-full-name
    abbreviation: MOFN
    url: https://www.my-organization.ca/my-organization-info-page
    email: info@my-organization.ca
    logo_path: ../assets/img/my-organization-logo.jpg
    endpoint: $ENDPOINT_URL

    connection:
      type: TheOrgBook
      api_url: $TOB_API_URL
      sign_target: false

    wallet:
      name: ${POSTGRESQL_WALLET_NAME:-myorg_issuer}
      seed: $WALLET_SEED_VONX
      type: $WALLET_TYPE
      params:
        storage_config:
          url: "$POSTGRESQL_WALLET_HOST:$POSTGRESQL_WALLET_PORT"
      access_creds:
        key: $WALLET_ENCRYPTION_KEY
        storage_credentials:
          account: $POSTGRESQL_WALLET_USER
          password: $POSTGRESQL_WALLET_PASSWORD
          admin_account: ${POSTGRESQL_WALLET_ADMIN_USER:-postgres}
          admin_password: $POSTGRESQL_WALLET_ADMIN_PASSWORD
        key_derivation_method: ARGON2I_MOD
```

- There is usually just a single issuer in the `issuer` structure, but there could be more.
- The issuer entry (`my-organization`) must have the same value as the organization part of the `routes.yml` paths.
- The issuer metadata (`name`, `url`, `abbreviation` and `email`) is presented on the OrgBook screen about the issuer.
- An optional logo for the issuer must be found in the repo at the relative location provided.
- The `endpoint` is the based URL for this agent. In this example, the value comes from an environment variable set elsewhere (perhaps in the `manage` script).
- The `connection` structure should also be as listed above.
  - The `sign_target` setting can be set to 1 (true) if out going requests should be signed
- The `wallet` structure contains information needed to configure the agent's own wallet. Those parameters are documented in Hyperledger Indy and depend on the wallet implementation you use.  BC Gov uses the Postgres implementation that we developed and contributed to the `indy-sdk` repo.


``` YAML
    credential_types:
    - description: Permit
      schema: my-permit.my-organization.ca
      issuer_url: http://localhost:5001/my-organization/my-permit
      depends_on:
        - greenlight_registration
        - pst_number
      credential:
        effective_date:
          input: effective_date
          from: claim

      topic:
        source_id:
          input: corp_num
          from: claim
        type:
          input: registration
          from: value

      # cardinality_fields:
      #   - address_type
```

The `credential_types` structure is repeated for each credential issued by the agent. The structure is within the `issuers` structure at the same level as the `wallet` and `connection` elements.  Some notes:

- The `description` element is credential metadata
- `schema` must match one of the schema `name` values in the `schemas.yml` file
- `issuer_url` must match the `path` value in the `routes.yml` file for route for the credential using the same schema
- `depends_on` defines the prerequisite proofs that must be satisfied before a credential can be issued. The depends_on list of values are references to `proof_requests` later in the file (described below) 
  - **NOTE**: When the VON issuer/verifier web form is invoked for a credential, the proof requests for that credential are executed, and the form is not displayed if the proofs are not succcessful. However, there is no requirement that an agent complete the proof requests prior to issuing a credential. It is the responsibility of the agent and the service driving the agent to make sure that the business requirements and data values are correct, whether or not the prerequisite proofs are completed.
- `effective_date` is an OrgBook concept that drives the timeline feature, setting when a particular credential came into affect, regardless of when it was issued to OrgBook. The value tells OrgBook how to get that value for this credential. In this case, it is being pulled from a claim in the credential called `effective_date` (clever name!).
  - OrgBook does not want to use `now()` as the effective date since, especially on initial loading, existing and historical credentials will be issued to OrgBook in bulk. Ideally, we can get the effective date from the credential. Failing that, some other business rule could be used, including just setting it to `now()`.
- `topic` is the mechanism to link a credential to its subject entity (see notes at the start of this section about "subject entities"). The mapping indicates the claim from which to map the data, and the name used by this instance of OrgBook, in this case `registration`.
  - Each instance of OrgBook could use a different name for the topic of the subject entity, and there could be multiple `topic` types in a single OrgBook instance.
- `cardinality_fields` is a list of attributes from the credential that are combined with the `topic` to define the cardinality (unique key) of the credential. See the notes at the start of this section about cardinality.
  - An example of the use of cardinality can be [seen here](https://github.com/bcgov/von-bc-registries-agent/blob/686c82c4274b2b2dca7f12922ecb947491665822/bcreg-x/config/services.yml#L228). In this example, the cardinality is on the topic (attribute `registration_id`) and the `address_type` attribute. Example:
    - If two credentials were issued for the same organization (same `registration_id`) and both had `Headquarters` as the `address_type` value, OrgBook would assume the latter was a reissued credential and would deactivate the earlier one, keeping it for historical purposes.
    - However, if one credential had an `address_type` of `Headquarters` and the other `Mailing`, both credentials would be considered `active`.

The final section of the `credential_types` structure are the mappings, an example of which follows below.

``` YAML
      mapping:
        - model: name
          fields:
            text:
              input: legal_name
              from: claim
            type:
              input: org_name
              from: value

        - model: attribute
          fields:
            type:
              input: issued_date
              from: value
            format:
              input: datetime
              from: value
            value:
              input: permit_issued_date
              from: claim
```

- Each mapping references a specific, concrete model that has been coded into OrgBook - either `name`, `address` or `attribute`.
  - `name` enables text searching for entities (e.g. organizations on [https://orgbook.gov.bc.ca](https://orgbook.gov.bc.ca)).
  - `address` enables location searching for entities. As of this writing, we have not enabled location searching in any production instance of OrgBook.
    - An example of the use of an address model can be [seen here](https://github.com/bcgov/von-bc-registries-agent/blob/686c82c4274b2b2dca7f12922ecb947491665822/bcreg-x/config/services.yml#L228)
  - `attribute` enables referencing a named variable in OrgBook such that the variable can be referenced in OrgBook UI. There are a couple of common use cases for this:
    - To define common elements of credentials, such as dates (effective, issued, expiration, etc.), such that they can be generically displayed on the OrgBook "Credential" screen, while still able to mapped for each credential type. This prevents us from using "magic attributes" in all credentials that always mean the same thing.
    - To define key elements of important, specific credentials, usually the foundational credential (for example, a business registration) that can be coded into the user interface of OrgBook. Note that when this is done, that instance of OrgBook has some hard-coded knowledge about specific credentials.
- The `type` part of the mapping defines the name used for this model within OrgBook. All VON issuer/verifier agents targeting the same OrgBook instance should use the same `type` names when referencing the same concepts.
- The `text` (for the `name` model), `value` (for the `attribute` model) and address fields (for the `address` model) provide the mapping for the incoming credential to the `type` of the model.
- The attribute model has an extra piece of metadata, the `format` of the attribute value (either `date` or `text`).

The final section of the `services.yml` includes sections on verifiers and on proof_requests that makes use of the verifiers.

``` YAML

verifiers:
  bctob:
    name: BC OrgBook
    connection:
      type: TheOrgBook
      api_url: $TOB_API_URL
    wallet:
      seed: "tob-verifier-wallet-000000000001"

proof_requests:
  # This Agent's DID - for proof requests based on this Issuer's Credentials
  #      X3tCbZSE9uUb223KYDWd6o
  greenlight_registration:
    version: '1.0.1'
    schemas:
      - key:
          did: 6qnvgJtqwK44D8LFYnV5Yf
          name: registration.greenlight
          version: '1.0.1'
        attributes:
          - corp_num
          - legal_name

```

- The `verifiers` contains a name (`bctob` in this case), and some details about the instance of OrgBook to which the agent connects.
  - The name of the verifier must match the `connection_id` element of the `proof_request` section of `routes.yml`
- `proof_requests` is a list of proof requests associated with credentials earlier in the `services.yml` file and in the `routes.yml` file.
  - The `version1 field is...
  - The `schemas` is a list of Hyperledger Indy schema keys (DID of the creator of the schema, its name and version) and an optional list of attributes to be included in the proof requests.
    - While not currently supported, we expect to add support for zero knowledge proofs of specific claims&mdash;that is, that a date is less than five years ago without revealing the date itself.
    - If no attributes are provided, the proof request is still performed to prove that the necessary credential is held without revealing the contents of the credential.
