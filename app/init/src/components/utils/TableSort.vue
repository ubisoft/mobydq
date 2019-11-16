<template>
  <span class="ml-1">
    <span
      class="sort"
      v-bind:class="{ active: columnName == sortAttribute.columnName && sortAttribute.sortOrder == 'asc' }"
      v-on:click="sort(columnName, 'asc')"
      >▲</span
    >
    <span
      class="sort"
      v-bind:class="{ active: columnName == sortAttribute.columnName && sortAttribute.sortOrder == 'desc' }"
      v-on:click="sort(columnName, 'desc')"
      >▼</span
    >
  </span>
</template>

<script>
export default {
  props: {
    columnName: String,
    sortAttribute: Object
  },
  methods: {
    sort(columnName, sortOrder) {
      let payload = {
        columnName: columnName,
        sortOrder: sortOrder
      };
      this.$emit("sortAttribute", payload);
    }
  }
};
</script>

<style>
span.sort {
  cursor: pointer;
  font-size: 0.75rem;
  color: #6c757d;
  background-color: transparent;
}
span.sort:hover {
  color: white;
  background-color: transparent;
}
span.active {
  color: white;
}
</style>
