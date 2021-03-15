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
          Schema Label:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Label"
            v-model="schemaLabel"
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
          Schema Name:
        </v-list-item-title>
        <v-list-item-subtitle>
          <v-text-field
            class="mt-6"
            placeholder="Name"
            v-model="schemaName"
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
          <vue-tags-input
            class="mt-6"
            v-model="schemaAttributes"
            :tags="tags"
            :validation="tagValidation"
            placeholder="List of attributes. Alphanumeric, '_' or '-' only"
            @tags-changed="newTags => tags = newTags"
          />
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
import VueTagsInput from '@johmun/vue-tags-input';

export default {
  name: "CreateSchema",
  components: {VueTagsInput},
  created: () => {},
  data: () => {
    return {
      schema: undefined,
      schemaLabel: "",
      schemaName: "",
      schemaVersion: "",
      schemaAttributes: "",
      tags: [],
      isBusyCreateSchema: false,
      rules: {
        required: (value) => !!value || "Can't be empty",
        version: (value) => (value && /^\d+(\.\d+){0,2}$/.test(value)) || "Schema Version must be numbers and '.'",
        schemaText: (value) => (value && /^[a-zA-Z\d-_]+$/.test(value)) || "Schema name and attributes must be alphanumeric and '_' or '-'"
      },
      tagValidation: [
        {
          classes: 'invalid-tag',
          rule: /^[a-zA-Z\d-_]+$/,
          disableAdd: true
        }
      ]
    };
  },
  computed: {
    fieldsEmpty() {
      return (
        this.schemaLabel.length === 0 || this.schemaName.length === 0 || this.schemaVersion.length === 0 || this.tags.length === 0
      );
    },
  },
  methods: {
    fixSchemaParams(s) {
      return s.trim().replace(/ /g, "_");
    },
    createSchema() {
      this.isBusyCreateSchema = true;

      const attrs = this.tags.map(s => this.fixSchemaParams(s));

      const data = {
        schemaLabel: this.schemaLabel,
        schemaName: this.fixSchemaParams(this.schemaName),
        schemaVersion: this.fixSchemaParams(this.schemaVersion),
        attributes: attrs
      };

      this.$axios
        .post(`${this.$apiBaseUrl}/admin/schema/create`, data)
        .then((result) => {
          console.log(result);
          this.isBusyCreateSchema = false;

          if (result.status === 200 || result.status === 200) {
            EventBus.$emit("success", "Schema created successfully");
            this.$router.push({ name: "SchemaSettings" });
            this.$store.dispatch("loadSchemas");
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
