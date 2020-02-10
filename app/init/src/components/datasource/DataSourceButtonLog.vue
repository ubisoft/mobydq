<template>
  <!-- Use router-link rather than v-on:click to allow user to open page in new window -->
  <router-link v-bind:to="'/datasources/' + dataSourceId + '/logs'">
    <button v-if="show" type="button" class="btn btn-secondary ml-1">
      Logs
    </button>
  </router-link>
</template>

<script>
export default {
  props: {
    dataSourceId: Number
  },
  computed: {
    show() {
      let roles = ["standard", "advanced", "admin"];
      return Number.isInteger(this.dataSourceId) && roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
