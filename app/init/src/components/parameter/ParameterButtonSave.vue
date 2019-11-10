<template>
  <button v-if="show" type="button" class="btn btn-success float-right" v-on:click="saveParameter">
    Save
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    indicatorId: Number,
    parameter: Object
  },
  methods: {
    saveParameter() {
      // Method to create or update a parameter
      // If parameter.id exists, update existing parameter
      if (this.parameter.id) {
        let payload = {
          query: this.$store.state.mutationUpdateParameter,
          variables: {
            id: this.parameter.id,
            parameterPatch: {
              parameterTypeId: this.parameter.parameterTypeId,
              value: this.parameter.value
            }
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
              this.parameter.updatedDate = response.data.data.updateParameterById.parameter.updatedDate;
              this.parameter.userByUpdatedById.email = response.data.data.updateParameterById.parameter.userByUpdatedById.email;
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
      // If parameter.id does not exist, create a new parameter
      else {
        let payload = {
          query: this.$store.state.mutationCreateParameter,
          variables: {
            parameter: {
              indicatorId: this.indicatorId,
              parameterTypeId: this.parameter.parameterTypeId,
              value: this.parameter.value
            }
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
              this.$emit("addParameter", response.data.data.createParameter.parameter);
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
    }
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
