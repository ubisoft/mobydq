<template>
  <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="resetPassword">
    Reset Password
  </button>
</template>

<script>
export default {
  props: {
    dataSourceId: String
  },
  methods: {
    resetPassword() {
      this.$emit("resetPassword", true);
    }
  },
  computed: {
    show() {
      let roles = ["advanced", "admin"];
      return this.dataSourceId != "new" && roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
