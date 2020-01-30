<template>
  <div class="col">
    <h1 class="mt-5">Logs</h1>
    <log></log>
  </div>
</template>

<script>
import log from "./log/Log.vue";

export default {
  components: {
    "log": log
  }
};
</script>
