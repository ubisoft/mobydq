<template>
  <span>
    <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="execute" v-bind:disabled="!flagActive" v-bind:readonly="!flagActive">
      Execute
    </button>
  </span>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    indicatorGroupId: Number,
    indicatorId: Number,
    flagActive: Boolean
  },
  data: function() {
    return {
    };
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return Number.isInteger(this.indicatorId) && roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    execute(){
      let payload = {
        query: this.$store.state.mutationExecuteIndicator,
        variables: {
          indicatorGroupId: this.indicatorGroupId,
          indicatorId: [this.indicatorId]
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
            let batch = response.data.data.executeBatch.batch;
            let session = {
              batchId: batch.id,
              batchByBatchId: { status: batch.status },
              id: batch.sessionsByBatchId.nodes[0].id,
              status: batch.sessionsByBatchId.nodes[0].status,
              nbRecords: batch.sessionsByBatchId.nodes[0].nbRecords,
              nbRecordsAlert: batch.sessionsByBatchId.nodes[0].nbRecordsAlert,
              nbRecordsNoAlert: batch.sessionsByBatchId.nodes[0].nbRecordsNoAlert
            };
            this.$emit("executeIndicator", session);  // Send batch to parent component
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
