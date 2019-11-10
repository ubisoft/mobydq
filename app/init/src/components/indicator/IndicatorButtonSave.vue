<template>
  <button v-if="show" type="button" class="btn btn-success" v-on:click="saveIndicator">
    Save
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    indicator: Object
  },
  methods: {
    saveIndicator() {
      // Method to create or update an indicator
      // If indicator.id exists, update existing indicator
      if (this.indicator.id) {
        let payload = {
          query: this.$store.state.mutationUpdateIndicator,
          variables: {
            id: this.indicator.id,
            indicatorPatch: {
              name: this.indicator.name,
              description: this.indicator.description,
              indicatorTypeId: this.indicator.indicatorTypeId,
              indicatorGroupId: this.indicator.indicatorGroupId,
              executionOrder: parseInt(this.indicator.executionOrder),
              flagActive: this.indicator.flagActive
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
              this.indicator.updatedDate = response.data.data.updateIndicatorById.indicator.updatedDate;
              this.indicator.userByUpdatedById.email = response.data.data.updateIndicatorById.indicator.userByUpdatedById.email;
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
      // If indicator.id does not exist, create a new indicator
      else {
        let payload = {
          query: this.$store.state.mutationCreateIndicator,
          variables: {
            indicator: {
              name: this.indicator.name,
              description: this.indicator.description,
              indicatorTypeId: this.indicator.indicatorTypeId,
              indicatorGroupId: this.indicator.indicatorGroupId,
              executionOrder: parseInt(this.indicator.executionOrder),
              flagActive: this.indicator.flagActive
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
              // Capture new indicator Id in case user wants to delete or update it
              this.indicator.id = response.data.data.createIndicator.indicator.id;
              this.$router.push({
                name: "edit-indicator",
                params: {
                  indicatorId: this.indicator.id
                }
              });
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
