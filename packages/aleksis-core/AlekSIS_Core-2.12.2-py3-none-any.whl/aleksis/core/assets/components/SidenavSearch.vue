<script>
export default {
  methods: {
    submit: function () {
      this.$refs.form.submit();
    },
  },
  props: {
    action: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      required: true,
    },
  },
  name: "SidenavSearch",
};
// FIXME: implement suggestions etc, use "loading" attribute
</script>

<template>
  <form method="get" ref="form" :action="action" id="search-form">
    <v-text-field
      :append-icon="'mdi-magnify'"
      @click:append="submit"
      single-line
      id="search"
      name="q"
      type="search"
      enterkeyhint="search"
      :placeholder="placeholder"
    ></v-text-field>
  </form>
</template>
