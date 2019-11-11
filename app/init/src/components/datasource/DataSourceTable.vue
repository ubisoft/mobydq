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
            Type
          </th>
          <th scope="col">
            Status
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dataSource in dataSources" v-bind:key="dataSource.id">
          <td>
            {{ dataSource.name }}
          </td>
          <td>
            {{ dataSource.dataSourceTypeByDataSourceTypeId.name }}
          </td>
          <td>
              <span class="badge badge-pill" v-bind:class="cssClass(dataSource.connectivityStatus)" >
                {{ dataSource.connectivityStatus }}
              </span>
          </td>
          <td>
            <router-link v-if="showEditDataSource" class="badge badge-secondary" v-bind:to="'/datasources/' + dataSource.id">
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
    dataSources: Array,
    sortAttribute: Object
  },
  computed: {
    showEditDataSource() {
      let roles = ["advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    setSortAttribute(attribute) {
      this.$emit("sortAttribute", attribute);
    },
    cssClass(status) {
      let cssClass;
      if(status == 'Success') {
        cssClass = 'badge-success';
      } else if (status == 'Failed') {
        cssClass = 'badge-danger';
      }
      return cssClass;
    }
  }
};
</script>
