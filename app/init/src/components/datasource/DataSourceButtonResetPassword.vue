<template>
  <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="resetPassword">
    Reset Password
  </button>
</template>

<script>
export default {
  props: {
    dataSourceId: Number
  },
  methods: {
    resetPassword() {
      this.$emit("resetPassword", true);
    }
  },
  computed: {
    show() {
      let roles = ["advanced", "admin"];
      return Number.isInteger(this.dataSourceId) && roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
