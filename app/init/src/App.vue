<template>
  <div id="app">
    <!-- Sidebar -->
    <sidebar></sidebar>
    
    <!-- Header -->
    <header-bar></header-bar>
    <error-message></error-message>

    <!-- Content -->
    <div id="main">
      <router-view :key="$route.fullPath"></router-view>
    </div>
  </div>
</template>

<script>
import HeaderBar from "./components/header/HeaderBar.vue";
import ErrorMessage from "./components/utils/ErrorMessage.vue";
import Sidebar from "./components/sidebar/Sidebar.vue";

export default {
  name: "app",
  components: {
    "header-bar": HeaderBar,
    "error-message": ErrorMessage,
    "sidebar": Sidebar
  },
  computed: {
    setCurrentUser() {
      // Set current user in store to manage UI display based on permissions
      // This also ensure user is not disconnected when refreshing the page
      let currentUser = {};
      if (this.$session.exists()) {
        currentUser = {
          isAuthenticated: true,
          role: this.$session.get("role"),
        };
      } else {
        currentUser = {
          isAuthenticated: false,
          role: "anonymous",
        };
      }
      this.$store.commit("setCurrentUser", currentUser);
      return currentUser;
    }
  },
  created() {
    this.setCurrentUser;
  }
};
</script>

<style>
#main {
  margin-left: 250px;
  padding-left: 20px;
  padding-right: 20px;
}

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
