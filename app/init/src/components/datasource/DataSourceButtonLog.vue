<template>
  <!-- Use router-link rather than v-on:click to allow user to open page in new window -->
  <router-link v-bind:to="'/logs/datasources/' + dataSourceId">
    <button type="button" class="btn btn-secondary ml-1">
      Logs
    </button>
  </router-link>
</template>

<script>
export default {
  props: {
    dataSourceId: Number
  }
};
</script>
