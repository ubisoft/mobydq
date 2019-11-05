<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless">
      <thead>
        <tr>
          <th scope="col">
            Name
            <table-sort v-bind:columnName="'name'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Indicator Type
          </th>
          <th scope="col">
            Indicator Group
          </th>
          <th scope="col">
            Active
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="indicator in indicators" v-bind:key="indicator.id">
          <td>
            {{ indicator.name }}
          </td>
          <td>
            {{ indicator.indicatorTypeByIndicatorTypeId.name }}
          </td>
          <td>
            {{ indicator.indicatorGroupByIndicatorGroupId.name }}
          </td>
           <td>
            {{ indicator.flagActive }}
          </td>
          <td>
            <router-link v-if="showEditIndicator" class="badge badge-secondary" v-bind:to="'/indicators/' + indicator.id">
              Edit Indicator
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import TableSort from "../utils/TableSort.vue";

export default {
  components: {
    "table-sort": TableSort
  },
  props: {
    indicators: Array,
    sortAttribute: Object
  },
  computed: {
    showEditIndicator() {
      let roles = ["admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    setSortAttribute(attribute) {
      this.$emit("sortAttribute", attribute);
    }
  }
};
</script>
