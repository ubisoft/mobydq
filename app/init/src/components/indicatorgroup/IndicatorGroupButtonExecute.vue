<template>
  <span>
    <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="execute">
      Execute
    </button>
  </span>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    indicatorGroupId: Number
  },
  data: function() {
    return {
    };
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return Number.isInteger(this.indicatorGroupId) && roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    execute(){
      let payload = {
        query: this.$store.state.mutationExecuteIndicatorGroup,
        variables: {
          indicatorGroupId: this.indicatorGroupId
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
            this.$emit("executeIndicatorGroup", batch);  // Send batch to parent component
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
