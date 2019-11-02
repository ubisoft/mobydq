<template>
  <div class="col">
    <h1 class="mt-5">Users</h1>
    <user-button-create></user-button-create>
    <user-search></user-search>
  </div>
</template>

<script>
import UserButtonCreate from "./user/UserButtonCreate.vue";
import UserSearch from "./user/UserSearch.vue";

export default {
  components: {
    "user-button-create": UserButtonCreate,
    "user-search": UserSearch
  }
};
</script>
