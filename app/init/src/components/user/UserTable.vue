<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless">
      <thead>
        <tr>
          <th scope="col">
            E-mail
            <table-sort v-bind:columnName="'email'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Role
            <table-sort v-bind:columnName="'role'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
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
        <tr v-for="user in users" v-bind:key="user.id">
          <td>
            <router-link v-bind:to="'/admin/users/' + user.id">
              {{ user.email }}
            </router-link>
          </td>
          <td>
            {{ user.role }}
          </td>
          <td>
            {{ user.flagActive }}
          </td>
          <td>
            <router-link v-if="showEditUser" class="badge badge-secondary" v-bind:to="'/admin/users/' + user.id">
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
    users: Array,
    sortAttribute: Object
  },
  computed: {
    showEditUser() {
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
