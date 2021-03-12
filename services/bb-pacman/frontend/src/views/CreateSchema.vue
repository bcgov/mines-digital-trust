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
        <span>Create Schema</span>
      </v-card-title>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
          Schema Name:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Name"
            v-model="schemaName"
            :rules="[rules.required]"
            outlined
            dense
            required
          >
          </v-text-field>
        </v-list-item-subtitle>
      </v-list-item>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
          Schema Version:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="0.0.0"
            v-model="schemaVersion"
            :rules="[rules.required, rules.version]"
            outlined
            dense
            required
          >
          </v-text-field>
        </v-list-item-subtitle>
      </v-list-item>
      <v-list-item>
        <v-list-item-title class="grey--text text--darken-2 font-weight-medium">
          Attributes:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Comma separated values"
            v-model="schemaAttributes"
            :rules="[rules.required]"
            outlined
            dense
            required
          >
          </v-text-field>
        </v-list-item-subtitle>
      </v-list-item>
      <v-card-actions>
        <v-layout justify-end>
          <v-btn
            :loading="this.isBusyCreateSchema"
            :disabled="fieldsEmpty"
            color="primary"
            @click="createSchema"
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
  name: "CreateSchema",
  components: {},
  created: () => {},
  data: () => {
    return {
      schema: undefined,
      schemaName: "",
      schemaVersion: "",
      schemaAttributes: "",
      isBusyCreateSchema: false,
      rules: {
        required: (value) => !!value || "Can't be empty",
        version: (value) => (value && /^\d+(\.\d+){0,2}$/.test(value)) || "Schema must be numbers and '.'"
      },
    };
  },
  computed: {
    fieldsEmpty() {
      return (
        this.schemaName.length === 0 || this.schemaVersion.length === 0 || this.schemaAttributes.length === 0
      );
    },
  },
  methods: {
    createSchema() {
      this.isBusyCreateSchema = true;

      const data = {
        schemaName: this.schemaName,
        schemaVersion: this.schemaVersion,
        attributes: this.schemaAttributes.split(",")
      };

      this.$axios
        .post(`${this.$apiBaseUrl}/admin/schema/create`, data)
        .then((result) => {
          console.log(result);
          this.isBusyCreateSchema = false;

          if (result.status === 200 || result.status === 200) {
            EventBus.$emit("success", "Schema created successfully");
            this.$router.push({ name: "SchemaSettings" });
          }
        })
        .catch((e) => {
          this.isBusyCreateSchema = false;
          if (e.response.status === 400) {
            EventBus.$emit("error", "Schema already exists");
          } else {
            console.error(e);
            EventBus.$emit("error", e);
          }
        });
    },
  },
};
</script>
