<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless">
      <thead>
        <tr>
          <th scope="col">
            Session Id
            <table-sort v-bind:columnName="'id'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Indicator Name
          </th>
          <th scope="col">
            Status
            <table-sort v-bind:columnName="'status'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Updated Date
            <table-sort v-bind:columnName="'updatedDate'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Created By
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="session in sessions" v-bind:key="session.id">
          <td>
            {{ session.id }}
          </td>
          <td>
            <router-link v-bind:to="'/indicators/' + session.indicatorId">
              {{ session.indicatorByIndicatorId.name }}
            </router-link>
          </td>
          <td>
            <router-link class="badge badge-pill" v-bind:class="statusCssClass(session.status)" v-bind:to="'/indicators/' + session.indicatorId">
              {{ session.status }}
            </router-link>
          </td>
          <td>
            {{ session.updatedDate }}
          </td>
          <td>
            {{ session.userByCreatedById.email }}
          </td>
          <td>
            <!-- <span v-if="showKillSession" class="badge badge-secondary">
              Kill
            </span> -->
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
    sessions: Array,
    sortAttribute: Object
  },
  computed: {
    showKillSession() {
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
