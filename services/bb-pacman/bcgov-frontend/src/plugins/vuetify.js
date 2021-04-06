// style.scss imports our font awesome styles and material design styles
import Vue from "vue";
import Vuetify from "vuetify";

import {
  mdiViewDashboard, mdiForumOutline, mdiAccountCircle, mdiBriefcaseVariant, mdiFingerprint,
  mdiWallet, mdiCog, mdiCardAccountDetailsOutline, mdiChevronLeft, mdiDelete, mdiContentCopy, mdiPlus, mdiPencil,
  mdiChevronRight, mdiCheck, mdiRefresh, mdiImport, mdiEye, mdiEyeOff, mdiBrightness1, mdiShapePolygonPlus
} from '@mdi/js';

Vue.use(Vuetify);

export default new Vuetify({
  defaultAssets: {
    font: true,
    icons: 'md'
  },
  icons: {
    iconfont: 'fa',
    values: {
      user: mdiAccountCircle,
      identity: mdiFingerprint,
      dashboard: mdiViewDashboard,
      profile: mdiCardAccountDetailsOutline,
      wallet: mdiWallet,
      credentialManagement: 'fas fa-exchange-alt',
      connections: mdiBriefcaseVariant,
      notifications: mdiForumOutline,
      settings: mdiCog,
      signout: 'fas fa-sign-out-alt',
      prev: mdiChevronLeft,
      next: mdiChevronRight,
      delete: mdiDelete,
      copy: mdiContentCopy,
      add: mdiPlus,
      pencil: mdiPencil,
      fingerprint: mdiFingerprint,
      check: mdiCheck,
      refresh: mdiRefresh,
      import: mdiImport,
      public: mdiEye,
      private: mdiEyeOff,
      partnerState: mdiBrightness1,
      newMessage: mdiShapePolygonPlus
    }
  },
  theme: {
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: '#003366',
        secondary: '#FCBA19',
        anchor: '#1A5A96',
        accent: '#82B1FF',
        error: '#D8292F',
        info: '#2196F3',
        success: '#2E8540',
        warning: '#FFC107'
      }
    }
  }
});
