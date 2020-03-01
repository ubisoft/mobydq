<template>
  <span>
    <button type="button" class="btn btn-secondary ml-1" v-on:click="markAllNotificationsAsRead">
      Mark all as read
    </button>
  </span>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  methods: {
    markAllNotificationsAsRead() {
      let payload = {
        query: this.$store.state.mutationMarkAllNotificationsAsRead
      };
      let headers = {};
      if (this.$session.exists()) {
        headers = { Authorization: "Bearer " + this.$session.get("jwt") };
      }
      this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
        function(response) {
          if (response.data.errors) {
            this.displayError(response);
          } else {
            this.$emit("markAllNotificationsAsRead", true);
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    }
  }
};
</script>
