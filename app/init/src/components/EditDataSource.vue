<template>
  <div class="col-5">
    <data-source-form></data-source-form>
  </div>
</template>

<script>
import DataSourceForm from "./datasource/DataSourceForm.vue";

export default {
  components: {
    "data-source-form": DataSourceForm
  }
};
</script>
