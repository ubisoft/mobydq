<template>
  <div class="col-5">
    <user-form></user-form>
  </div>
</template>

<script>
import UserForm from "./user/UserForm.vue";

export default {
  components: {
    "user-form": UserForm
  }
};
</script>
