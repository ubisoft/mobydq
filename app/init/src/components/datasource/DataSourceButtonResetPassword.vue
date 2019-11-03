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
      return this.dataSourceId != "new";
    }
  }
};
</script>
