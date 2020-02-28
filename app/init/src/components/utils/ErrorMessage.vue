<template>
  <div id="errorMessage" v-bind:class="cssClass">
    <div class="justify-content-center alert alert-danger alert-dismissable text-danger">
      Error: {{ errorMessage }}
      <button type="button" class="close" v-on:click="close()">
        &times;
      </button>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    cssClass() {
      if (this.$store.state.errorObject.flag) {
        return "display";
      } else {
        return "d-none";
      }
    },
    errorMessage() {
      return this.$store.state.errorObject.message;
    }
  },
  methods: {
    close() {
      this.$store.state.errorObject.flag = false;
      this.$store.state.errorObject.message = "";
    }
  }
};
</script>

<style scoped>
#errorMessage {
  margin-left: 250px;
}
</style>