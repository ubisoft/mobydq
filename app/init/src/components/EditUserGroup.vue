<template>
  <div class="col-5">
    <user-group-form></user-group-form>
  </div>
</template>

<script>
import UserGroupForm from "./usergroup/UserGroupForm.vue";

export default {
  components: {
    "user-group-form": UserGroupForm
  }
};
</script>
