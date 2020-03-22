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
            <router-link v-bind:to="'/indicators/' + indicator.id">
              {{ indicator.name }}
            </router-link>
          </td>
          <td>
            {{ indicator.indicatorTypeByIndicatorTypeId.name }}
          </td>
          <td>
            <router-link v-bind:to="'/indicatorgroups/' + indicator.indicatorGroupId">
              {{ indicator.indicatorGroupByIndicatorGroupId.name }}
            </router-link>
          </td>
           <td>
            {{ indicator.flagActive }}
          </td>
          <td>
            <router-link v-if="showEditIndicator" class="badge badge-secondary" v-bind:to="'/indicators/' + indicator.id">
              Edit
            </router-link>
            <a v-if="showEditIndicator && indicator.flagActive" class="badge badge-secondary ml-1" v-on:click="execute(indicator.indicatorGroupId, indicator.id)">
              Execute
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
    indicators: Array,
    sortAttribute: Object
  },
  computed: {
    showEditIndicator() {
      let roles = ["standard", "advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    setSortAttribute(attribute) {
      this.$emit("sortAttribute", attribute);
    },
    execute(indicatorGroupId, indicatorId){
      let payload = {
        query: this.$store.state.mutationExecuteIndicator,
        variables: {
          indicatorGroupId: indicatorGroupId,
          indicatorId: [indicatorId]
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
            //this.$emit("executedIndicator", ...);  // Send test status to parent component
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
