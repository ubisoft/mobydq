<template>
  <!-- Use router-link rather than v-on:click to allow user to open page in new window -->
  <router-link v-if="show" v-bind:to="'indicators/new'">
    <button type="button" class="btn btn-success">
      Create Indicator
    </button>
  </router-link>
</template>

<script>
export default {
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
