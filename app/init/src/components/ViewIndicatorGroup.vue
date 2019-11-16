<template>
  <div class="col">
    <h1 class="mt-5">Indicator Groups</h1>
    <indicator-group-button-create></indicator-group-button-create>
    <indicator-group-search></indicator-group-search>
  </div>
</template>

<script>
import IndicatorGroupButtonCreate from "./indicatorgroup/IndicatorGroupButtonCreate.vue";
import IndicatorGroupSearch from "./indicatorgroup/IndicatorGroupSearch.vue";

export default {
  components: {
    "indicator-group-button-create": IndicatorGroupButtonCreate,
    "indicator-group-search": IndicatorGroupSearch
  }
};
</script>
