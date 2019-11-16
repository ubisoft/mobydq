<template>
  <div class="col">
    <h1 class="mt-5">Indicators</h1>
    <indicator-button-create></indicator-button-create>
    <indicator-search></indicator-search>
  </div>
</template>

<script>
import IndicatorButtonCreate from "./indicator/IndicatorButtonCreate.vue";
import IndicatorSearch from "./indicator/IndicatorSearch.vue";

export default {
  components: {
    "indicator-button-create": IndicatorButtonCreate,
    "indicator-search": IndicatorSearch
  }
};
</script>
