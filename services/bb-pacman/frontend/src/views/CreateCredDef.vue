<!--
 Copyright (c) 2020 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/hyperledger-labs/organizational-agent

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <v-container>
    <v-card max-width="600" class="mx-auto">
      <v-card-title class="bg-light">
        <v-btn depressed color="secondary" icon @click="$router.go(-1)">
          <v-icon dark>mdi-chevron-left</v-icon>
        </v-btn>
        <span>Create Credential Definition</span>
      </v-card-title>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
          Schema Id:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Schema Id"
            v-model="schemaId"
            :rules="[rules.required]"
            outlined
            dense
            required
            readonly
            disabled
          >
          </v-text-field>
        </v-list-item-subtitle>
      </v-list-item>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
          Tag:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Tag"
            v-model="tag"
            :rules="[rules.required,rules.schemaText]"
            outlined
            dense
            required
          >
          </v-text-field>
        </v-list-item-subtitle>
      </v-list-item>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
          Revocation Registry Size:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Revocation Registry Size (integer)"
            v-model="revocationRegistrySize"
            :rules="[rules.required, rules.sized]"
            outlined
            dense
            required
            disabled
          >
          </v-text-field>
        </v-list-item-subtitle>
      </v-list-item>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-checkbox
            class="mt-6"
            label="Support Revocation"
            v-model="supportRevocation"
            outlined
            dense
            disabled
          >
          </v-checkbox>
        </v-list-item-subtitle>
      </v-list-item>
      <v-card-actions>
        <v-layout justify-end>
          <v-btn
            :loading="this.isBusyCreateCredDef"
            :disabled="fieldsEmpty"
            color="primary"
            @click="createCredDef"
          >
            Submit
          </v-btn>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
  import { EventBus } from "../main";
  export default {
    name: "CreateCredDef",
    props: {
      schemaId: String
    },
    components: {},
    created: () => {
    },
    data: () => {
      return {
        credDef: undefined,
        tag: "default",
        supportRevocation: false,
        revocationRegistrySize: 4,
        isBusyCreateCredDef: false,
        rules: {
          required: (value) => !!value || "Can't be empty",
          sized: (value) => (value && /^\d+$/.test(value) && (value >= 4 && value <= 32768)) || "Size must be integer between 4 and 32768",
          schemaText: (value) => (value && /^[a-zA-Z\d-_]+$/.test(value)) || "Value must be alphanumeric and '_' or '-'"
        }
      };
    },
    computed: {
      fieldsEmpty() {
        return (
          this.schemaId.length === 0 || this.tag.length === 0 || this.revocationRegistrySize < 4 || this.revocationRegistrySize > 32768
        );
      },
    },
    methods: {
      fixParams(s) {
        return s.trim().replace(/ /g, "_");
      },
      createCredDef() {
        this.isBusyCreateCredDef = true;

        const data = {
          schemaId: this.schemaId,
          tag: this.fixParams(this.tag),
          supportRevocation: this.supportRevocation,
          revocationRegistrySize: this.revocationRegistrySize
        };

        this.$axios
          .post(`${this.$apiBaseUrl}/admin/creddef`, data)
          .then((result) => {
            this.isBusyCreateCredDef = false;

            if (result.status === 200 || result.status === 200) {
              EventBus.$emit("success", "Credential Definition created successfully");
              this.$store.dispatch("loadSchemas");
              this.$store.dispatch("loadCredDefs");
              this.$router.go(-1);
            }
          })
          .catch((e) => {
            this.isBusyCreateCredDef = false;
            if (e.response.status === 400) {
              EventBus.$emit("error", "Credential Definition already exists");
            } else {
              EventBus.$emit("error", e);
            }
          });
      },
    },
  };
</script>
