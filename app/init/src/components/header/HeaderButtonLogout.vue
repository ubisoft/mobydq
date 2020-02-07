<template>
  <button v-if="show" class="btn btn-outline-secondary ml-1" v-on:click="logout">
    Logout
  </button>
</template>

<script>
export default {
  methods: {
    logout() {
      this.$session.destroy();
      // Reset current user
      let currentUser = {
        isAuthenticated: false,
        role: "anonymous"
      };
      this.$store.commit("setCurrentUser", currentUser);
      this.$router.push({
        name: "home"
      });
    }
  },
  computed: {
    show() {
      return this.$store.state.currentUser.isAuthenticated;
    }
  }
};
</script>
