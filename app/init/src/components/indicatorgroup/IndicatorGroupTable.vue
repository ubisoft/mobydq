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
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="indicatorGroup in indicatorGroups" v-bind:key="indicatorGroup.id">
          <td>
            {{ indicatorGroup.name }}
          </td>
          <td>
            <router-link v-if="showEditIndicatorGroup" class="badge badge-secondary" v-bind:to="'/indicatorgroups/' + indicatorGroup.id">
              Edit
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
    indicatorGroups: Array,
    sortAttribute: Object
  },
  computed: {
    showEditIndicatorGroup() {
      let roles = ["standard", "advanced", "admin"];
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
