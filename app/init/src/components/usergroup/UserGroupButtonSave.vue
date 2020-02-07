<template>
  <button v-if="show" type="button" class="btn btn-success" v-on:click="saveUserGroup">
    Save
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    userGroup: Object
  },
  methods: {
    saveUserGroup() {
      // Method to create or update a user group
      // If userGroup.id exists, update existing user group
      if (this.userGroup.id) {
        let payload = {
          query: this.$store.state.mutationUpdateUserGroup,
          variables: {
            id: this.userGroup.id,
            userGroupPatch: {
              name: this.userGroup.name
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
              this.userGroup.updatedDate = response.data.data.updateUserGroupById.userGroup.updatedDate;
              this.userGroup.userByUpdatedById.email = response.data.data.updateUserGroupById.userGroup.userByUpdatedById.email;
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
      // If userGroup.id does not exist, create a new user group
      else {
        let payload = {
          query: this.$store.state.mutationCreateUserGroup,
          variables: {
            userGroup: {
              name: this.userGroup.name
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
              // Capture new user group Id in case user wants to delete or update it
              this.userGroup.id = response.data.data.createUserGroup.userGroup.id;
              this.$router.push({
                name: "edit-user-group",
                params: {
                  userGroupId: this.userGroup.id
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
      let roles = ["admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
