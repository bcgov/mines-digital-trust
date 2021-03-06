<!--
 Copyright (c) 2020 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/hyperledger-labs/organizational-agent

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <v-container>
    <v-card v-if="isReady" class="mx-auto">
      <v-card-title class="bg-light">
        <v-btn depressed icon @click="$router.go(-1)">
          <v-icon dark>$vuetify.icons.prev</v-icon>
        </v-btn>
        <div v-if="presentation.type === CredentialTypes.UNKNOWN.type">
          {{ presentation.credentialDefinitionId | credentialTag }}
        </div>
        <div v-else>
          {{ presentation.typeLabel }}
        </div>
      </v-card-title>
      <v-card-text>
        <Cred v-bind:document="presentation" isReadOnly></Cred>
        <v-divider></v-divider>
      </v-card-text>
      <v-card-actions>
        <v-expansion-panels v-if="expertMode" accordion flat>
          <v-expansion-panel>
            <v-expansion-panel-header
              class="grey--text text--darken-2 font-weight-medium bg-light"
              >Show raw data</v-expansion-panel-header
            >
            <v-expansion-panel-content class="bg-light">
              <vue-json-pretty :data="presentation"></vue-json-pretty>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-actions>

      <!-- <v-card-actions>
      <v-layout align-end justify-end>
        <v-btn color="secondary" text @click="cancel()">Cancel</v-btn>
        <v-btn :loading="this.isBusy" color="primary" text @click="saveChanges()">Save</v-btn>
      </v-layout>
    </v-card-actions> -->
    </v-card>
  </v-container>
</template>

<script>
import { EventBus } from "../main";

import Cred from "@/components/Credential";
import { CredentialTypes } from "../constants";

export default {
  name: "IssuedCredentialPresentation",
  props: {
    id: String,
    credId: String,
  },
  created() {
    EventBus.$emit("title", "Issued Credential");
    this.getPresentation();
  },
  data: () => {
    return {
      document: {},
      isBusy: false,
      isReady: false,
      CredentialTypes: CredentialTypes,
    };
  },
  computed: {
    expertMode() {
      return this.$store.state.expertMode;
    },
  },
  methods: {
    getPresentation() {
      this.$axios
        .get(
          `${this.$apiBaseUrl}/partners/${this.id}/issue-credential/${this.credId}`
        )
        .then((result) => {
          if ({}.hasOwnProperty.call(result, "data")) {
            this.presentation = result.data;
            this.isReady = true;
          }
        })
        .catch((e) => {
          console.error(e);
          EventBus.$emit("error", e);
        });
    },
    cancel() {
      this.$router.go(-1);
    },
  },
  components: {
    Cred,
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
