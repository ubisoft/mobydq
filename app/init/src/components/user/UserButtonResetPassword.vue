<template>
  <button v-if="show" type="button" class="btn btn-secondary ml-1" v-on:click="resetPassword">
    Reset Password
  </button>
</template>

<script>
export default {
  props: {
    userId: String
  },
  methods: {
    resetPassword() {
      this.$emit("resetPassword", true);
    }
  },
  computed: {
    show() {
      let roles = ["admin"];
      return this.userId != "new" && roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
