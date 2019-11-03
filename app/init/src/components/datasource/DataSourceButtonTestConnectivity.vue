<template>
  <span>
    <button v-if="show" type="button" class="btn btn-secondary ml-1">
      Test Connectivity
    </button>
  </span>
</template>

<script>

export default {
  props: {
    dataSourceId: String
  },
  computed: {
    show() {
      return this.dataSourceId != "new";
    }
  }
};
</script>
