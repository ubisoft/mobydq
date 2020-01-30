<template>
  <div class="modal fade" id="ModalBoxDuplicate" tabindex="-1" role="dialog" aria-labelledby="Duplicate" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal" role="document">
      <div class="modal-content bg-dark text-light">
        <div class="modal-header">
          <h5 class="modal-title">Duplicate Indicator</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body bg-secondary text-light">
          <div class="form-group required">
            <label for="indicatorName" class="col-form-label">
              Name:
            </label>
            <input
              class="form-control col-sm"
              id="newIndicatorName"
              type="text"
              required="required"
              placeholder="Type new indicator name"
              v-model="newIndicatorName"
              v-bind:disabled="isReadOnly"
              v-bind:readonly="isReadOnly"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-success" v-on:click="duplicate" data-dismiss="modal">
            Duplicate
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
    indicatorId: Number
  },
  data: function() {
    return {
      newIndicatorName: ''
    };
  },
  computed: {
    isReadOnly() {
      let roles = ["standard", "advanced", "admin"];
      return !roles.includes(this.$store.state.currentUser.role);
    }
  },
  methods: {
    duplicate() {
      let payload = {
        query: this.$store.state.mutationDuplicateIndicator,
        variables: {
          indicatorId: this.indicatorId,
          newIndicatorName: this.newIndicatorName
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
            let newIndicatorId = response.data.data.duplicateIndicator.indicator.id;
              this.$router.push({
                name: "edit-indicator",
                params: {
                  indicatorId: newIndicatorId
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
