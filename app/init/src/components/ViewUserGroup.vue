<template>
  <div class="col">
    <h1 class="mt-5">User Groups</h1>
    <user-group-button-create></user-group-button-create>
    <user-group-search></user-group-search>
  </div>
</template>

<script>
import UserGroupButtonCreate from "./usergroup/UserGroupButtonCreate.vue";
import UserGroupSearch from "./usergroup/UserGroupSearch.vue";

export default {
  components: {
    "user-group-button-create": UserGroupButtonCreate,
    "user-group-search": UserGroupSearch
  }
};
</script>
