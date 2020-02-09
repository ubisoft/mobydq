<template>
  <button v-if="show" type="button" class="btn btn-danger" v-on:click="deleteObject" data-dismiss="modal">
    Delete
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    parameterId: Number
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return Number.isInteger(this.parameterId) && roles.includes(this.$store.state.currentUser.role);
    }
  },
   methods: {
    deleteObject() {
      // Method to delete object
      let payload = {
        query: this.$store.state.mutationDeleteParameter,
        variables: {
          id: this.parameterId
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
            // Send new parameter to parent to update parameter table
            this.$emit("removeParameter", this.parameterId);
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
