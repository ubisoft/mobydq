<template>
  <div id="app">
    <header-bar></header-bar>
    <error-message></error-message>

    <div class="container-fluid">
      <div id="main" class="row justify-content-center">
        <router-view :key="$route.fullPath"></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderBar from "./components/header/HeaderBar.vue";
import ErrorMessage from "./components/utils/ErrorMessage.vue";

export default {
  name: "app",
  components: {
    "header-bar": HeaderBar,
    "error-message": ErrorMessage
  },
  computed: {
    currentUser() {
      // Set current user in store to manage UI display based on permissions
      if (this.$session.exists()) {
        this.$store.state.currentUser.isAuthenticated = true;
        this.$store.state.currentUser.role = this.$session.get("role");
        this.$store.state.currentUser.userGroups = this.$session.get("userGroups");
        this.$store.state.currentUser.selectedUserGroup = this.$session.get("selectedUserGroup");
      } else {
        this.$store.state.currentUser.isAuthenticated = false;
        this.$store.state.currentUser.role = "anonymous";
      }
      return this.$store.state.currentUser;
    }
  },
  created() {
    this.currentUser; // Trigger get user session on page refresh
  }
};
</script>

<style>
/*Style for required fields*/
.form-group.required .col-form-label:after {
  content: "*";
  color: OrangeRed;
}
.form-control::-webkit-input-placeholder {
  color: #bfbfbf;
} /* WebKit, Blink, Edge */
.form-control:-moz-placeholder {
  color: #bfbfbf;
} /* Mozilla Firefox 4 to 18 */
.form-control::-moz-placeholder {
  color: #bfbfbf;
} /* Mozilla Firefox 19+ */
.form-control:-ms-input-placeholder {
  color: #bfbfbf;
} /* Internet Explorer 10-11 */
.form-control::-ms-input-placeholder {
  color: #bfbfbf;
} /* Microsoft Edge */

/*Style for readonly fields*/
.form-control[readonly] {
  background-color: #a7a7a7;
  border-color: #6c757d;
}
</style>
