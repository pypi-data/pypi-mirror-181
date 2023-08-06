<template>
  <v-menu offset-y>
    <template #activator="{ on, attrs }">
      <v-btn depressed v-bind="attrs" v-on="on" color="primary">
        <v-icon icon color="white">mdi-translate</v-icon>
        {{ $i18n.locale }}
      </v-btn>
    </template>
    <v-list id="language-dropdown" class="dropdown-content" min-width="150">
      <v-skeleton-loader
        v-if="!$root.systemProperties.availableLanguages"
        class="mx-auto"
        type="list-item, list-item, list-item"
      ></v-skeleton-loader>
      <v-list-item-group
        v-if="$root.systemProperties.availableLanguages"
        v-model="$i18n.locale"
        color="primary"
      >
        <v-list-item
          v-for="languageOption in $root.systemProperties.availableLanguages"
          :key="languageOption.code"
          :value="languageOption.code"
          @click="setLanguage(languageOption)"
        >
          <v-list-item-title>{{
            languageOption.nameTranslated
          }}</v-list-item-title>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  data: function () {
    return {
      language: this.$i18n.locale,
    };
  },
  methods: {
    setLanguage: function (languageOption) {
      document.cookie = languageOption.cookie;
      this.$i18n.locale = languageOption.code;
      this.$vuetify.lang.current = languageOption.code;
    },
  },
  name: "LanguageForm",
};
</script>
