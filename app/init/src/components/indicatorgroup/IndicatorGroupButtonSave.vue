<template>
  <button v-if="show" type="button" class="btn btn-success" v-on:click="saveIndicatorGroup">
    Save
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    indicatorGroup: Object
  },
  methods: {
    saveIndicatorGroup() {
      // Method to create or update an indicator group
      // If indicatorGroup.id exists, update existing indicator group
      if (this.indicatorGroup.id) {
        let payload = {
          query: this.$store.state.mutationUpdateIndicatorGroup,
          variables: {
            id: this.indicatorGroup.id,
            indicatorGroupPatch: {
              name: this.indicatorGroup.name
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
              this.indicatorGroup.updatedDate = response.data.data.updateIndicatorGroupById.indicatorGroup.updatedDate;
              this.indicatorGroup.userByUpdatedById.email = response.data.data.updateIndicatorGroupById.indicatorGroup.userByUpdatedById.email;
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
      // If indicatorGroup.id does not exist, create a new indicator group
      else {
        let payload = {
          query: this.$store.state.mutationCreateIndicatorGroup,
          variables: {
            indicatorGroup: {
              name: this.indicatorGroup.name
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
              // Capture new indicator group Id in case user wants to delete or update it
              this.indicatorGroup.id = response.data.data.createIndicatorGroup.indicatorGroup.id;
              this.$router.push({
                name: "edit-indicator-group",
                params: {
                  indicatorGroupId: this.indicatorGroup.id
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
