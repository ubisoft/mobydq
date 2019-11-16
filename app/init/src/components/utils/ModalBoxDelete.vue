<template>
  <div class="modal fade" id="ModalBoxDelete" tabindex="-1" role="dialog" aria-labelledby="Delete" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm" role="document">
      <div class="modal-content bg-dark text-light">
        <div class="modal-header">
          <h5 class="modal-title">Watch Out!</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body bg-secondary text-light">
          This operation cannot be undone. <br />
          Are you sure you want to delete this?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="deleteObject" data-dismiss="modal">
            Delete
          </button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";

export default {
  mixins: [Mixins],
  props: {
    objectType: String,
    objectId: Number
  },
  methods: {
    deleteObject() {
      // Get mutation for each type of object
      let mutation, route;
      if (this.objectType == "dataSource") {
        mutation = this.$store.state.mutationDeleteDataSource;
        route = { name: "view-data-source" };
      }
      else if (this.objectType == "indicatorGroup") {
        mutation = this.$store.state.mutationDeleteIndicatorGroup;
        route = { name: "view-indicator-group" };
      }
      else if (this.objectType == "indicator") {
        mutation = this.$store.state.mutationDeleteIndicator;
        route = { name: "view-indicator" };
      }
      else if (this.objectType == "parameter") {
        mutation = this.$store.state.mutationDeleteParameter;
      }

      // Method to delete object
      let payload = {
        query: mutation,
        variables: {
          id: this.objectId
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
            this.$router.push(route);
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

<style>
.modal-header {
  border: 0px;
}
.modal-footer {
  border: 0px;
}
</style>
