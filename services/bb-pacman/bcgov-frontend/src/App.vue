<!--
 Copyright (c) 2020 - for information on the respective copyright owner
 see the NOTICE file and/or the repository at
 https://github.com/hyperledger-labs/organizational-agent

 SPDX-License-Identifier: Apache-2.0
-->
<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <router-link tag="span" :to="{ name: 'Dashboard' }">
          <v-list-item v-if="logo" two-line class="pl-3 mt-n2">
            <v-list-item-content>
              <v-list-item-title
                ><v-img v-if="logo" :src="logo"></v-img
              ></v-list-item-title>
              <v-list-item-subtitle>Business Partner Agent</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-else two-line class="pl-3 mt-n2" >
            <v-list-item-avatar style="width: fit-content">
              <v-icon>$vuetify.icons.user</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <!-- <v-list-item-title>{{ getAgentName }}</v-list-item-title> -->
              <!-- <v-list-item-subtitle></v-list-item-subtitle> -->
            </v-list-item-content>
          </v-list-item>
        </router-link>
        <v-list-item v-if="expertMode" link :to="{ name: 'Identity' }">
          <v-list-item-action>
            <v-icon>$vuetify.icons.identity</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Identity</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link :to="{ name: 'Dashboard' }" exact>
          <v-list-item-action>
            <v-icon>$vuetify.icons.dashboard</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link :to="{ name: 'PublicProfile' }">
          <v-list-item-action>
            <v-icon>$vuetify.icons.profile</v-icon>
          </v-list-item-action>
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item>
        <v-list-item link :to="{ name: 'Wallet' }">
          <v-list-item-action>
            <v-badge
              overlap
              bordered
              :content="newCredentialsCount"
              :value="newCredentialsCount"
              color="red"
              offset-x="10"
              offset-y="10"
            >
              <v-icon>$vuetify.icons.wallet</v-icon>
            </v-badge>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Wallet</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link :to="{ name: 'CredentialManagement' }" style="display: none">
          <v-list-item-action>
            <v-icon>$vuetify.icons.credentialManagement</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Credential Management</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link :to="{ name: 'Partners' }">
          <v-list-item-action>
            <v-badge
              overlap
              bordered
              :content="newPartnersCount"
              :value="newPartnersCount"
              color="red"
              offset-x="10"
              offset-y="10"
            >
              <v-icon>$vuetify.icons.connections</v-icon>
            </v-badge>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Connections</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link :to="{ name: 'Notifications' }" style="display: none">
          <v-list-item-action>
            <v-icon>$vuetify.icons.notifications</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Notifications</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-divider></v-divider>
        <v-list dense>
          <v-list-item link :to="{ name: 'Settings' }">
            <v-list-item-action>
              <v-icon>$vuetify.icons.settings</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Settings</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="logout()">
            <v-list-item-action>
              <v-icon>$vuetify.icons.signout</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Sign out</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

    <v-app-bar color="primary" app flat dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>{{ getTitle }}</v-toolbar-title>

      <v-spacer></v-spacer>

      <a href="https://www2.gov.bc.ca" data-test="btn-header-logo">
        <v-img
          alt="B.C. Government Logo"
          class="d-none d-sm-flex d-md-none"
          contain
          height="3.5rem"
          src="@/assets/images/bc_logo_square.svg"
          width="3.5rem"
        />
        <v-img
          alt="B.C. Government Logo"
          class="d-none d-md-flex"
          contain
          height="3.5rem"
          src="@/assets/images/bc_logo.svg"
          width="10rem"
        />
      </a>

    </v-app-bar>

    <v-main>
      <app-taa v-if="!sessionDialog && $store.getters.taaRequired"></app-taa>
      <router-view
        v-if="!sessionDialog && !$store.getters.taaRequired"
      ></router-view>
    </v-main>

    <v-snackbar
      v-model="snackbar"
      :bottom="true"
      :color="color"
      :multi-line="false"
      :right="true"
      :timeout="5000"
      :top="false"
      :vertical="true"
    >
      {{ snackbarMsg }}
      <v-btn dark text @click="snackbar = false">Close</v-btn>
    </v-snackbar>

    <v-dialog v-model="sessionDialog" max-width="290">
      <v-card>
        <v-card-title class="headline">Session expired</v-card-title>

        <v-card-text
          >It seems your session is expired. Do you want log in
          again?</v-card-text
        >

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="warning" text @click="sessionDialog = false">No</v-btn>

          <v-btn color="green darken-1" text @click="logout()">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import { EventBus } from "./main";
import Taa from "./components/taa/TransactionAuthorAgreement";

export default {
  components: {
    "app-taa": Taa
  },
  props: {
    source: String,
  },
  data: () => ({
    title: "",
    drawer: null,
    logo: process.env.VUE_APP_LOGO_URL,

    // snackbar stuff
    snackbar: false,
    color: "",
    snackbarMsg: "",

    sessionDialog: false,
  }),
  computed: {
    expertMode() {
      return this.$store.state.expertMode;
    },
    newPartnersCount() {
      return this.$store.getters.newPartnersCount;
    },
    newCredentialsCount() {
      return this.$store.getters.newCredentialsCount;
    },
    getAgentName() {
      let bpaName = "Business Partner Agent";
      const nameSettingValue = this.$store.getters.getSettingByKey("agentName");
      if (nameSettingValue) {
        bpaName = nameSettingValue;
      }
      return bpaName;
    },
    getTitle() {
      let pageTitle = (this.title && this.title.trim().length > 0) ? ` > ${this.title}` : "";
      return `${this.getAgentName} ${pageTitle}`;
    }
  },
  created() {
    this.$vuetify.theme.dark = false;
    this.$store.dispatch("validateTaa");

    // Global Error handling
    // Todo: Put in extra component

    EventBus.$on("title", (title) => {
      this.title = title;
    });

    EventBus.$on("success", (msg) => {
      (this.snackbarMsg = msg), (this.color = "green"), (this.snackbar = true);
    });

    EventBus.$on("error", (msg) => {
      console.log(msg.response);

      if (
        {}.hasOwnProperty.call(msg, "response") &&
        {}.hasOwnProperty.call(msg.response, "status")
      ) {
        switch (msg.response.status) {
          case 401:
            this.sessionDialog = true;
        }

        if (
          {}.hasOwnProperty.call(msg.response, "data") &&
          {}.hasOwnProperty.call(msg.response.data, "message")
        ) {
          msg = msg.response.data.message;
        }
      }

      (this.snackbarMsg = msg), (this.color = "red"), (this.snackbar = true);
    });
  },
  methods: {
    logout() {
      this.$axios
        .post(`${this.$apiBaseUrl}/logout`)
        .then(() => {
          location.reload();
        })
        .catch((e) => {
          console.error(e);
          location.reload();
        });
    },
  },
};
</script>
<style>
.bg-light {
  background-color: #fafafa;
}
</style>
