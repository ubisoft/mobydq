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
    dataSourceId: String
  },
  data: function() {
    return {
      connectivityTestStatus: {}
    };
  },
  computed: {
    show() {
      return this.dataSourceId != "new";
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
            this.connectivityTestStatus = response.data[1]['data']['dataSourceById'];
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
