<template>
  <div class="col">
    <h1 class="mt-5">Sessions</h1>
    <session-search></session-search>
  </div>
</template>

<script>
import SessionSearch from "./session/SessionSearch.vue";

export default {
  components: {
    "session-search": SessionSearch
  }
};
</script>
