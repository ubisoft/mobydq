<template>
  <div class="col">
    <h1 class="mt-5">Indicator Session Log</h1>
    <indicator-session-log></indicator-session-log>
  </div>
</template>

<script>
import IndicatorSessionLog from "./indicator/IndicatorSessionLog.vue";

export default {
  components: {
    "indicator-session-log": IndicatorSessionLog
  }
};
</script>
