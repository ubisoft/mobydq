<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless">
      <thead>
        <tr>
          <th scope="col">
            Name
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="membership in user.userGroupMembershipsByUserId.nodes" v-bind:key="membership.id">
          <td>
            {{ membership.userGroupByUserGroupId.name }}
          </td>
          <td>
            <span v-if="showRemoveUserGroup" class="badge badge-secondary" v-on:click="removeUserGroupMembership(membership.id)">
              Remove
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    user: Object
  },
  methods: {
    removeUserGroupMembership(id) {
      // Method to delete a relationship between a user and a user group
      let payload = {
        query: this.$store.state.mutationDeleteUserGroupMembership,
        variables: { id: id }
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
            this.$emit("removeUserGroupMembership", id);
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    }
  },
  computed: {
    showRemoveUserGroup() {
      let roles = ["admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>

<style>
.badge {
  cursor: pointer;
}
</style>
