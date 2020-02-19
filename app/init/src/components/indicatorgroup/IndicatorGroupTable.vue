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
            <router-link v-bind:to="'/indicatorgroups/' + indicatorGroup.id">
              {{ indicatorGroup.name }}
            </router-link>
          </td>
          <td>
            <router-link v-if="showEditIndicatorGroup" class="badge badge-secondary" v-bind:to="'/indicatorgroups/' + indicatorGroup.id">
              Edit
            </router-link>
            <a v-if="showEditIndicatorGroup" class="badge badge-secondary ml-1" v-on:click="execute(indicatorGroup.id)">
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
    },
    execute(indicatorGroupId){
      let payload = {
        query: this.$store.state.mutationExecuteIndicatorGroup,
        variables: {
          indicatorGroupId: indicatorGroupId
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
            //this.$emit("executedIndicatorGroup", ...);  // Send test status to parent component
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
