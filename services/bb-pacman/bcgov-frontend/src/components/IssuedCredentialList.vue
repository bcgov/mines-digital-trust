<!--
 Copyright (c) 2020 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/hyperledger-labs/organizational-agent

 SPDX-License-Identifier: Apache-2.0
-->

<template>
  <v-data-table
    :hide-default-footer="credentialsWithIndex.length < 10"
    v-model="selected"
    :show-select="selectable"
    :headers="headers"
    :items="credentialsWithIndex"
    :expanded.sync="expanded"
    item-key="index"
    :show-expand="expandable"
    :sort-by="['createdDate']"
    :sort-desc="[false]"
    single-select
    @click:row="openCredential"
  >
    <template v-slot:[`item.type`]="{ item }">
      <div v-if="item.type === CredentialTypes.UNKNOWN.type">
        {{ item.credentialDefinitionId | credentialTag | capitalize }}
      </div>
      <div v-else>
        {{ item.typeLabel }}
      </div>
    </template>
    <template v-slot:[`item.issuedAt`]="{ item }">
      {{ item.issuedAt | moment("YYYY-MM-DD HH:mm") }}
    </template>
    <template v-slot:[`item.state`]="{ item }">
      <v-icon
        v-if="item.state == 'credential_acked'"
        color="green"
        >$vuetify.icons.check</v-icon
      >
      <span v-else>
        {{ item.state.replace("_", " ") }}
      </span>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <Credential
          v-bind:document="item"
          isReadOnly
          showOnlyContent
        ></Credential>
      </td>
    </template>
  </v-data-table>
</template>

<script>
import Credential from "@/components/Credential";
import { CredentialTypes } from "../constants";
import { issuedListHeaders } from "@/components/tableHeaders/PresentationListHeaders";

export default {
  props: {
    credentials: Array,
    selectable: {
      type: Boolean,
      default: false,
    },
    expandable: {
      type: Boolean,
      default: true,
    },
    headers: {
      type: Array,
      default: () => issuedListHeaders,
    },
  },
  data: () => {
    return {
      selected: [],
      CredentialTypes: CredentialTypes,
      expanded: [],
    };
  },
  computed: {
    // Add an unique index, because elements do not have unique id
    credentialsWithIndex: function () {
      return this.credentials.map((creds, index) => ({
        ...creds,
        index: index + 1,
      }));
      // .map(credential => {
      //   credential.verified = true
      // })
    },
  },
  methods: {
    openCredential(item) {
      if (item.state == "credential_acked") {
        if (item.id) {
          this.$router.push({
            path: `issued/${item.id}`,
            append: true,
          });
        }
      } else {
        // Do nothing for now. Presentation is not ready
        // Need to fix Presentation.vue for unfinished presentations
      }
    },
  },
  components: {
    Credential,
  },
};
</script>
