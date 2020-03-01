<template>
  <span>
    <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="testConnectivity">
      Test
    </button>
  </span>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    dataSourceId: Number
  },
  computed: {
    show() {
      let roles = ["advanced", "admin"];
      return Number.isInteger(this.dataSourceId) && roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    testConnectivity() {
      let payload = {
        query: this.$store.state.mutationTestDataSource,
        variables: {
          dataSourceId: parseInt(this.dataSourceId)
        }
      };
      let headers = {};
      if (this.$session.exists()) {
        headers = { Authorization: "Bearer " + this.$session.get("jwt") };
      }
      this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
        function(response) {
          if (response.data.errors) {
            this.displayError(response);
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
