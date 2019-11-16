<template>
  <div>
    <h1 class="mt-5">User Groups</h1>

    <div class="form-group">
      <div class="w-50 float-left mr-2 mb-4">
        <treeselect
          placeholder="Select user groups"
          v-model="userGroups"
          v-bind:options="options"
          v-bind:multiple="true"
          v-bind:disable-branch-nodes="true"
          v-bind:disabled="isReadOnly"
          v-bind:readonly="isReadOnly"
        />
      </div>
      <user-button-add-user-group class="float-left" v-bind:user="user" v-bind:userGroups="userGroups" v-on:addUserGroupMembership="addUserGroupMembership">
      </user-button-add-user-group>
    </div>

    <user-user-group-table v-if="user.userGroupMembershipsByUserId" v-bind:user="user" v-on:removeUserGroupMembership="removeUserGroupMembership">
    </user-user-group-table>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import Treeselect from "@riophae/vue-treeselect";
import "@riophae/vue-treeselect/dist/vue-treeselect.css";
import UserButtonAddUserGroup from "./UserButtonAddUserGroup.vue";
import UserUserGroupTable from "./UserUserGroupTable.vue";

export default {
  mixins: [Mixins],
  components: {
    treeselect: Treeselect,
    "user-button-add-user-group": UserButtonAddUserGroup,
    "user-user-group-table": UserUserGroupTable
  },
  props: {
    user: Object
  },
  data() {
    return {
      userGroups: [],
      options: []
    };
  },
  computed: {
    isReadOnly() {
      let roles = ["admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    addUserGroupMembership(userGroupMembership) {
      this.$emit("addUserGroupMembership", userGroupMembership);
    },
    removeUserGroupMembership(id) {
      this.$emit("removeUserGroupMembership", id);
    }
  },
  created: function() {
    let payload = { query: this.$store.state.queryGetUserUserGroups };
    let headers = {};
    if (this.$session.exists()) {
      headers = { Authorization: "Bearer " + this.$session.get("jwt") };
    }
    this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
      function(response) {
        if (response.data.errors) {
          this.displayError(response);
        } else {
          this.options = response.data.data.allUserGroups.nodes;
        }
      },
      // Error callback
      function(response) {
        this.displayError(response);
      }
    );
  }
};
</script>

<style>
.vue-treeselect {
  color: #666666;
}
</style>
