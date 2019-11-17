<template>
  <div class="mt-4">
    <table class="table table-striped table-dark table-hover table-borderless table-sm">
      <thead>
        <tr>
          <th scope="col">
            Session Id
            <table-sort v-bind:columnName="'id'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Status
            <table-sort v-bind:columnName="'status'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Nb Records
          </th>
          <th scope="col">
            Nb Alerts
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
            <span class="badge badge-pill" v-bind:class="cssClass(session.status)" >
              {{ session.status }}
            </span>
          </td>
          <td>
          </td>
          <td>
          </td>
          <td>
            <router-link class="badge badge-secondary" v-bind:to="'/sessions/' + session.id">
              View
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
    sessions: Array,
    sortAttribute: Object
  },
  computed: {
  },
  methods: {
    setSortAttribute(attribute) {
      this.$emit("sortAttribute", attribute);
    },
    cssClass(status) {
      let cssClass;
      if (status == 'Pending') {
        cssClass = 'badge-secondary';
      } else if(status == 'Running') {
        cssClass = 'badge-info';
      } else if(status == 'Success') {
        cssClass = 'badge-success';
      } else if (status == 'Failed') {
        cssClass = 'badge-danger';
      }
      return cssClass;
    },
  }
};
</script>
