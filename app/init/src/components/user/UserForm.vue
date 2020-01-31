<template>
  <div>
    <h1 class="mt-5">Edit User</h1>

    <form>
      <div class="form-row">
        <div class="col-11">
          <!-- User Form -->
          <div class="form-group required">
            <label for="userEmail" class="col-form-label">
              E-mail:
            </label>
            <input
              class="form-control col-sm"
              id="userEmail"
              type="email"
              required="required"
              placeholder="Type user e-mail"
              v-model="user.email"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>

          <div v-if="showPasswordField" class="form-group">
            <label for="userPassword" class="col-form-label">
              Password:
            </label>
            <input
              class="form-control col-sm"
              id="userPassword"
              type="password"
              required="true"
              placeholder="Type user password"
              v-model="user.password"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>

          <div class="form-group required">
            <label for="userRole" class="col-form-label">
              Role:
            </label>
            <select
              class="form-control"
              id="userRole"
              required="true"
              v-model="user.role"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly">
                <option disabled value="">Select user role</option>
                <option value="standard">standard</option>
                <option value="advanced">advanced</option>
                <option value="admin">admin</option>
            </select>
          </div>

          <div class="custom-control custom-switch mr-4 mt-1 mb-2">
            <input
              class="custom-control-input"
              id="active"
              type="checkbox"
              value=""
              v-model="user.flagActive"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
            <label for="active" class="custom-control-label">
              Active
            </label>
          </div>

          <!-- Meta-Data -->
          <div>
            <user-meta-data
              v-if="user.id"
              v-bind:id="user.id"
              v-bind:createdDate="user.createdDate"
              v-bind:createdBy="user.userByCreatedById.email"
              v-bind:updatedDate="user.updatedDate"
              v-bind:updatedBy="user.userByUpdatedById.email"
            ></user-meta-data>
          </div>

          <!-- Button Menu -->
          <div class="mt-3">
              <user-button-save v-bind:user="user" v-bind:showPasswordField="showPasswordField"> </user-button-save>
              <user-button-reset-password v-on:resetPassword="resetPassword" v-bind:userId="userId"> </user-button-reset-password>
              <user-button-close> </user-button-close>
            </div>
          </div>
        </div>

      <!-- User Groups -->
      <div class="form-group required">
        <user-user-group
          v-if="user.id"
          v-bind:user="user"
          v-on:addUserGroupMembership="addUserGroupMembership"
          v-on:removeUserGroupMembership="removeUserGroupMembership"
        ></user-user-group>
      </div>
    </form>
  </div>
</template>

<script>
import UserButtonSave from "./UserButtonSave.vue";
import UserButtonResetPassword from "./UserButtonResetPassword.vue";
import UserButtonClose from "./UserButtonClose.vue";
import UserUserGroup from "./UserUserGroup.vue";
import MetaDataCard from "../utils/MetaDataCard.vue";
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  components: {
    "user-button-save": UserButtonSave,
    "user-button-reset-password": UserButtonResetPassword,
    "user-button-close": UserButtonClose,
    "user-meta-data": MetaDataCard,
    "user-user-group": UserUserGroup
  },
  data: function() {
    return {
      user: { flagActive: true },
      showPasswordField: false
    };
  },
  computed: {
    userId() {
      return parseInt(this.$route.params.userId.toString());
    },
    isReadOnly() {
      let roles = ["admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    addUserGroupMembership(userGroupMembership) {
      this.user.userGroupMembershipsByUserId.nodes.push(userGroupMembership);
    },
    removeUserGroupMembership(id) {
      let memberships = this.user.userGroupMembershipsByUserId.nodes;
      for (let i = 0; i < memberships.length; i++) {
        if (memberships[i]["id"] == id) {
          this.user.userGroupMembershipsByUserId.nodes.splice(i, 1);
        }
      }
    },
    resetPassword(value) {
      this.showPasswordField = value;
    }
  },
  created: function() {
    // If userId != new then get data for existing user
    if (Number.isInteger(this.userId)) {
      let payload = {
        query: this.$store.state.queryGetUser,
        variables: {
          id: parseInt(this.userId)
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
            this.user = response.data.data.userById;
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    } else {
      this.showPasswordField = true;
    }
  }
};
</script>
