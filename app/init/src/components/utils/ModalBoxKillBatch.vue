<template>
  <div class="modal fade" id="ModalBoxKillBatch" tabindex="-1" role="dialog" aria-labelledby="Kill" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-m" role="document">
      <div class="modal-content bg-dark text-light">
        <div class="modal-header">
          <h5 class="modal-title">Watch Out!</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body bg-secondary text-light">
          This will cancel all incomplete sessions in <b>batch Id {{batchId}}</b><br />
          Are you sure you want to kill the batch?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="killBatch" data-dismiss="modal">
            Kill
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
    batchId: Number
  },
  methods: {
    killBatch() {
      // Method to kill a batch
      let payload = {
        query: this.$store.state.mutationKillBatch,
        variables: {
          batchId: this.batchId
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
            // Do nothing
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
