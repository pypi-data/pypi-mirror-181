<template>
  <message-box :value="cache" type="warning">
    {{ $t("alerts.page_cached") }}
  </message-box>
</template>

<script>
export default {
  name: "CacheNotification",
  data() {
    return {
      cache: false,
    };
  },
  created() {
    this.channel = new BroadcastChannel("cache-or-not");
    this.channel.onmessage = (event) => {
      this.cache = event.data === true;
    };
  },
  destroyed() {
    this.channel.close();
  },
};
</script>
