<template>
  <div class="col">
    <h1 class="mt-5">Data Sources</h1>
    <data-source-button-create></data-source-button-create>
    <data-source-search></data-source-search>
  </div>
</template>

<script>
import DataSourceButtonCreate from "./datasource/DataSourceButtonCreate.vue";
import DataSourceSearch from "./datasource/DataSourceSearch.vue";

export default {
  components: {
    "data-source-button-create": DataSourceButtonCreate,
    "data-source-search": DataSourceSearch
  }
};
</script>
