import Vue from "vue";
import VueRouter from "vue-router";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";

import ApolloClient from "apollo-boost";
import VueApollo from "vue-apollo";

import "./css/global.scss";
import VueI18n from "vue-i18n";

import messages from "./messages.json";

Vue.use(VueI18n);

const i18n = new VueI18n({
  locale: "en",
  fallbackLocale: "en",
  messages,
});

// Using this function, apps can register their locale files
i18n.registerLocale = function (messages) {
  for (let locale in messages) {
    i18n.mergeLocaleMessage(locale, messages[locale]);
  }
};

Vue.use(Vuetify);
Vue.use(VueRouter);

const vuetify = new Vuetify({
  // TODO: load theme data dynamically
  //  - find a way to load template context data
  //  - include all site preferences
  //  - load menu stuff to render the sidenav
  icons: {
    iconfont: "mdi", // default - only for display purposes
    values: {
      cancel: "mdi-close-circle-outline",
      delete: "mdi-close-circle-outline",
      success: "mdi-check-circle-outline",
      info: "mdi-information-outline",
      warning: "mdi-alert-outline",
      error: "mdi-alert-octagon-outline",
      prev: "mdi-chevron-left",
      next: "mdi-chevron-right",
      checkboxOn: "mdi-checkbox-marked-outline",
      checkboxIndeterminate: "mdi-minus-box-outline",
      edit: "mdi-pencil-outline",
    },
  },
  theme: {
    dark:
      JSON.parse(document.getElementById("design-mode").textContent) === "dark",
    themes: {
      light: {
        primary: JSON.parse(
          document.getElementById("primary-color").textContent
        ),
        secondary: JSON.parse(
          document.getElementById("secondary-color").textContent
        ),
      },
      dark: {
        primary: JSON.parse(
          document.getElementById("primary-color").textContent
        ),
        secondary: JSON.parse(
          document.getElementById("secondary-color").textContent
        ),
      },
    },
  },
});

const apolloClient = new ApolloClient({
  uri: JSON.parse(document.getElementById("graphql-url").textContent),
});

import CacheNotification from "./components/CacheNotification.vue";
import LanguageForm from "./components/LanguageForm.vue";
import MessageBox from "./components/MessageBox.vue";
import NotificationList from "./components/notifications/NotificationList.vue";
import SidenavSearch from "./components/SidenavSearch.vue";

Vue.component(MessageBox.name, MessageBox); // Load MessageBox globally as other components depend on it

Vue.use(VueApollo);

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
});

const router = new VueRouter({
  mode: "history",
  //  routes: [
  //    { path: "/", component: "TheApp" },
  //  }
});

const app = new Vue({
  el: "#app",
  apolloProvider,
  vuetify: vuetify,
  // delimiters: ["<%","%>"] // FIXME: discuss new delimiters, [[ <% [{ {[ <[ (( …
  data: () => ({
    drawer: vuetify.framework.breakpoint.lgAndUp,
    group: null, // what does this mean?
    urls: window.Urls,
    django: window.django,
    // FIXME: maybe just use window.django in every component or find a suitable way to access this property everywhere
    showCacheAlert: false,
    systemProperties: {
      currentLanguage: "en",
      availableLanguages: [],
    },
  }),
  apollo: {
    systemProperties: require("./systemProperties.graphql"),
  },
  watch: {
    systemProperties: function (newProperties) {
      this.$i18n.locale = newProperties.currentLanguage;
      this.$vuetify.lang.current = newProperties.currentLanguage;
    },
  },
  components: {
    "cache-notification": CacheNotification,
    "language-form": LanguageForm,
    "notification-list": NotificationList,
    "sidenav-search": SidenavSearch,
  },
  router,
  i18n,
});

window.app = app;
window.router = router;
window.i18n = i18n;
