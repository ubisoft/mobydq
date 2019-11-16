<template>
  <div class="col">
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
