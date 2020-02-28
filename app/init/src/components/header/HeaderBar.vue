<template>
  <nav class="navbar text-light justify-content-between">
    <span class="navbar-brand"></span>

    <form class="form-inline">
      <header-button-notification></header-button-notification>
      <header-button-admin></header-button-admin>
      <header-button-login></header-button-login>
      <header-button-logout></header-button-logout>
    </form>
  </nav>
</template>

<script>
import HeaderButtonNotification from "./HeaderButtonNotification.vue";
import HeaderButtonAdmin from "./HeaderButtonAdmin.vue";
import HeaderButtonLogin from "./HeaderButtonLogin.vue";
import HeaderButtonLogout from "./HeaderButtonLogout.vue";

export default {
  components: {
    "header-button-notification": HeaderButtonNotification,
    "header-button-admin": HeaderButtonAdmin,
    "header-button-login": HeaderButtonLogin,
    "header-button-logout": HeaderButtonLogout
  }
};
</script>

<style>
.navbar {
  background-color: #353a40;
}
</style>
