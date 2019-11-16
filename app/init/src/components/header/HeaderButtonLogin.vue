<template>
  <router-link v-if="!show" to="/login">
    <button class="btn btn-secondary ml-1">
      Login
    </button>
  </router-link>
</template>

<script>
export default {
  computed: {
    show() {
      return this.$store.state.currentUser.isAuthenticated;
    }
  }
};
</script>
