<template>
  <button v-if="show" type="button" class="btn btn-success" v-on:click="saveUser">
    Save
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    user: Object,
    showPasswordField: Boolean
  },
  methods: {
    saveUser() {
      // Method to create or update a user
      // If user.id exists, update existing user
      if (this.user.id) {
        let payload = {
          query: this.$store.state.mutationUpdateUser,
          variables: {
            id: this.user.id,
            sysUserPatch: {
              email: this.user.email,
              role: this.user.role,
              flagActive: this.user.flagActive
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
              this.user.updatedDate = response.data.data.updateSysUserById.sysUser.updatedDate;
              this.user.sysUserByUpdatedById.email = response.data.data.updateSysUserById.sysUser.sysUserByUpdatedById.email;

              // Update password only if value is supplied by admin user
              if (this.showPasswordField && this.user.password) {
                this.updatePassword();
              }
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
      // If user.id does not exist, create a new user
      else {
        let payload = {
          query: this.$store.state.mutationCreateUser,
          variables: {
            sysUser: {
              email: this.user.email,
              role: this.user.role,
              flagActive: this.user.flagActive
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
              // Capture new user Id in case user wants to delete or update it
              this.user.id = response.data.data.createSysUser.sysUser.id;

              // Create password for the user
              this.createPassword();

              // Redirect to user page
              this.$router.push({
                name: "edit-user",
                params: {
                  userId: this.user.id
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
    },
    createPassword(){
      // Create password for the user
      let payload = {
        query: this.$store.state.mutationCreatePassword,
        variables: {
          sysPassword: {
            userId: this.user.id,
            password: this.user.password
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
            // Success
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    },
    updatePassword(){
      let payload = {
        query: this.$store.state.mutationUpdatePassword,
        variables: {
          userId: this.user.id,
          sysPasswordPatch: {
            password: this.user.password
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
            // Success
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
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
