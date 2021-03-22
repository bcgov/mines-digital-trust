<!--
 Copyright (c) 2020 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/hyperledger-labs/organizational-agent

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <v-container>
    <v-card class="mx-auto">
      <v-card-title class="bg-light">
        <v-btn depressed color="secondary" icon @click="$router.go(-1)">
          <v-icon dark>mdi-chevron-left</v-icon>
        </v-btn>
        Issue a Credential
      </v-card-title>

      <v-card-text>
        <h4 class="pt-4">Select a credential to issue</h4>
        <v-combobox
          v-model="selectedSchema"
          :items="schemaList"
          label=""
          outlined
          dense
          @change="schemaSelected"
        ></v-combobox>
      </v-card-text>

      <v-card-text>
      <h4 v-if="selectedSchema && selectedSchema.value && selectedSchema.value.schema">Credential Content</h4>
      <v-row>
        <v-col>
          <v-text-field
            v-for="field in selectedSchema.value.fields"
            :key="field.type"
            :label="field.label"
            placeholder
            :rules="[(v) => !!v || 'Item is required']"
            :required="field.required"
            outlined
            dense
            @change="fieldChanged(field.type, $event)"
          ></v-text-field>
        </v-col>
      </v-row>
      </v-card-text>
      <v-card-actions>
        <v-layout align-end justify-end>
          <v-btn color="secondary" text @click="cancel()">Cancel</v-btn>
          <v-btn
            :loading="this.isBusy"
            color="primary"
            text
            @click="issueCredential()"
            :disabled="fieldsEmpty"
          >Submit</v-btn
          >
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
  import { EventBus } from "../main";

  // import { CredentialTypes } from "../constants";
  //import MyCredentialList from "@/components/MyCredentialList";

  export default {
    name: "IssueCredential",
    components: {
      //MyCredentialList,
    },
    props: {
      id: String,
    },
    created() {
      EventBus.$emit("title", "Issue Credential");
      this.getSchemaList();
    },
    data: () => {
      return {
        isBusy: false,
        schemaList: [],
        selectedSchema: {text: '', value: {}},
        credentialFields: {},
        fieldsEmpty: true,
        credHeaders: [
          {
            text: "Label",
            value: "label",
          },
          {
            text: "Type",
            value: "type",
          },
          {
            text: "Issuer",
            value: "issuer",
          },
          {
            text: "Issued at",
            value: "issuedAt",
          },
        ],
      };
    },
    computed: {

    },
    methods: {
      getSchemaList() {
        // get schemas...
        // get cred defs
        // map together for  pick list
        var _schemas = [];
        var _creddefs = {};
        this.schemaList = [];
        this.$axios
          .get(`${this.$apiBaseUrl}/admin/schema`)
          .then((result) => {
            if ({}.hasOwnProperty.call(result, "data")) {
              _schemas = result.data;
            }
          })
          .then(() => { return this.$axios.get(`${this.$apiBaseUrl}/admin/creddef?map=true`) })
          .then((result) => {
            if ({}.hasOwnProperty.call(result, "data")) {
              _creddefs = result.data;
            }
            _schemas.forEach(d => {
              const cdef = _creddefs[d.schemaId];
              if (cdef) {
                const o = {
                  text: `${d.label} (${d.schemaId.split(':').reverse()[0]})`,
                  value: {
                    schema: d,
                    creddef: cdef,
                    fields: d.schemaAttributeNames.map((key) => {
                      return {
                        type: key,
                        label: key
                          ? key.substring(0, 1).toUpperCase() +
                          key.substring(1).replace(/([a-z])([A-Z])/g, "$1 $2")
                          : "",
                      };
                    })
                  }
                }
                this.schemaList.push(o);
              }
            });
            this.isBusy = false;
          })
          .catch((e) => {
            this.isBusy = false;
            if (e.response.status === 404) {
              this.schemaList = [];
            } else {
              console.error(e);
              EventBus.$emit("error", e);
            }
          });
      },

      schemaSelected() {
        this.credentialFields = {};
        this.fieldsEmpty = true;
      },

      fieldChanged(propertyName, event) {
        this.credentialFields[propertyName] = event;
        this.fieldsEmpty = !(event && event.trim().length> 0);
      },
      issueCredential() {
        this.isBusy = true;
        this.$axios
          .post(`${this.$apiBaseUrl}/partners/${this.id}/issue-credential/send`, {
            schemaId: this.selectedSchema.value.schema.schemaId,
            credentialDefinitionId: this.selectedSchema.value.creddef.id,
            document: this.credentialFields
          })
          .then((res) => {
            console.log(res);
            this.isBusy = false;
            EventBus.$emit("success", "Credential Issued");
            this.$router.push({
              name: "Partner",
              params: { id: this.id },
            });
          })
          .catch((e) => {
            this.isBusy = false;
            console.error(e);
            EventBus.$emit("error", e);
          });
      },

      cancel() {
        this.$router.go(-1);
      },
    },
  };
</script>

<style scoped>
  .bg-light {
    background-color: #fafafa;
  }

  .bg-light-2 {
    background-color: #ececec;
  }
</style>
