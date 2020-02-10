<template>
  <div class="col">
    <h1 class="mt-5">Login</h1>

    <!-- User Form -->
    <div class="form-group w-25">
      <label for="userEmail" class="col-form-label">
        E-mail:
      </label>
      <input class="form-control col-sm" id="userEmail" type="email" required="required" placeholder="Type user e-mail" v-model="credentials.email" />
    </div>
    <div class="form-group w-25">
      <label for="userPassword" class="col-form-label">
        Password:
      </label>
      <input class="form-control col-sm" id="userPassword" type="password" required="true" placeholder="Type user password" v-model="credentials.password" />
    </div>
    <button type="button" class="btn btn-success" v-on:click="authenticateUser">
      Login
    </button>
  </div>
</template>

<script>
import Mixins from "./utils/Mixins.vue";

export default {
  mixins: [Mixins],
  data: function() {
    return {
      credentials: {}
    };
  },
  methods: {
    authenticateUser() {
      // Method to authenticate a user and get a token
      let payload = {
        query: this.$store.state.mutationAuthenticateUser,
        variables: {
          userEmail: this.credentials.email,
          userPassword: this.credentials.password
        }
      };
      this.$http.post(this.$store.state.graphqlUrl, payload).then(
        function(response) {
          if (response.data.errors) {
            this.displayError(response);
          } else {
            let token = response.data.data.authenticateUser.token;
            if (token) {
              // Set session token
              this.$session.set("jwt", token);
              this.getCurrentUser();
              this.$router.push({
                name: "home"
              });
            } else {
              this.$store.state.errorObject.flag = true;
              this.$store.state.errorObject.message = "Authentication failed. Login or password incorrect or user account has been inactivated.";
            }
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    },
    getCurrentUser() {
      // Method to get authenticated user information
      let payload = {
        query: this.$store.state.queryGetCurrentUser,
        variables: { email: this.credentials.email }
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
            // Set current user, role, user groups in session object
            this.$session.set("email", response.data.data.userByEmail.email);
            this.$session.set("role", response.data.data.userByEmail.role);

            // Set current user, role, user groups in store
            let currentUser = {
              isAuthenticated: true,
              role: response.data.data.userByEmail.role
            };
            this.$store.commit("setCurrentUser", currentUser);
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
