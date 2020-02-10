<template>
  <span>
    <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="testConnectivity">
      Test Connectivity
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
  data: function() {
    return {
      connectivityTestStatus: {}
    };
  },
  computed: {
    show() {
      let roles = ["advanced", "admin"];
      return Number.isInteger(this.dataSourceId) && roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    testConnectivity(){
      this.connectivityTestStatus['spinner'] = true;
      this.$emit("connectivityTestStatus", this.connectivityTestStatus);
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
          } else {
            this.connectivityTestStatus = response.data.data.testDataSource.dataSource;
            this.connectivityTestStatus['spinner'] = false;
            this.$emit("connectivityTestStatus", this.connectivityTestStatus);  // Send test results to parent component
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
