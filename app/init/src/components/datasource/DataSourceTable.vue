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
            <router-link v-bind:to="'/datasources/' + dataSource.id">
              {{ dataSource.name }}
            </router-link>
          </td>
          <td>
            {{ dataSource.dataSourceTypeByDataSourceTypeId.name }}
          </td>
          <td>
            <router-link class="badge badge-pill" v-bind:class="statusCssClass(dataSource.connectivityStatus)" v-bind:to="'/datasources/' + dataSource.id">
              {{ dataSource.connectivityStatus }}
            </router-link>
          </td>
          <td>
            <router-link v-if="showEditDataSource" class="badge badge-secondary" v-bind:to="'/datasources/' + dataSource.id">
              Edit
            </router-link>
            <a v-if="showEditDataSource" class="badge badge-secondary ml-1" v-on:click="testConnectivity(dataSource.id)">
              Test
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import TableSort from "../utils/TableSort.vue";

export default {
  mixins: [Mixins],
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
    testConnectivity(dataSourceId) {
      let payload = {
        query: this.$store.state.mutationTestDataSource,
        variables: {
          dataSourceId: dataSourceId
        }
      };
      let headers = {};
      if (this.$session.exists()) {
        headers = { Authorization: "Bearer " + this.$session.get("jwt") };
      }
      this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
        function(response) {
          if (response.data.errors) {
            this.displayError(response);
          } else {
            // this.$emit("connectivityTestStatus", this.connectivityTestStatus); // Send test results to parent component
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    }
  }
};
</script>
