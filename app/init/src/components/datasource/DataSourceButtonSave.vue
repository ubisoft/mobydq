<template>
  <button v-if="show" type="button" class="btn btn-success" v-on:click="saveDataSource">
    Save
  </button>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    dataSource: Object,
    showPasswordField: Boolean
  },
  methods: {
    saveDataSource() {
      // Method to create or update a data source
      // If dataSource.id exists, update existing data source
      if (this.dataSource.id) {
        let payload = {
          query: this.$store.state.mutationUpdateDataSource,
          variables: {
            id: this.dataSource.id,
            dataSourcePatch: {
              name: this.dataSource.name,
              dataSourceTypeId: this.dataSource.dataSourceTypeId,
              connectionString: this.dataSource.connectionString,
              login: this.dataSource.login
            }
          }
        };

        // Update password only if value is supplied by user
        if (this.showPasswordField && this.dataSource.password) {
          payload.variables.dataSourcePatch['password'] = this.dataSource.password;
        }

        let headers = {};
        if (this.$session.exists()) {
          headers = { Authorization: "Bearer " + this.$session.get("jwt") };
        }
        this.$http.post(this.$store.state.graphqlUrl, payload, { headers }).then(
          function(response) {
            if (response.data.errors) {
              this.displayError(response);
            } else {
              this.dataSource.updatedDate = response.data.data.updateDataSourceById.dataSource.updatedDate;
              this.dataSource.userByUpdatedById.email = response.data.data.updateDataSourceById.dataSource.userByUpdatedById.email;
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
      // If dataSource.id does not exist, create a new data source
      else {
        let payload = {
          query: this.$store.state.mutationCreateDataSource,
          variables: {
            dataSource: {
              name: this.dataSource.name,
              dataSourceTypeId: this.dataSource.dataSourceTypeId,
              connectionString: this.dataSource.connectionString,
              login: this.dataSource.login,
              password: this.dataSource.password
            }
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
              // Capture new data source Id in case user wants to delete or update it
              this.dataSource.id = response.data.data.createDataSource.dataSource.id;
              this.$router.push({
                name: "edit-data-source",
                params: {
                  dataSourceId: this.dataSource.id
                }
              });
            }
          },
          // Error callback
          function(response) {
            this.displayError(response);
          }
        );
      }
    }
  },
  computed: {
    show() {
      let roles = ["advanced", "admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
