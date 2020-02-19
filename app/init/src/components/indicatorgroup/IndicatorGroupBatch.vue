<template>
  <div class="mt-4">
    <table class="table table-striped table-dark table-hover table-borderless table-sm">
      <thead>
        <tr>
          <th scope="col">
            Batch Id
          </th>
          <th scope="col">
            Status
          </th>
          <th scope="col">
            Nb Sessions
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="batch in batches" v-bind:key="batch.id">
          <td>
            {{ batch.id }}
          </td>
          <td>
            <router-link class="badge badge-pill" v-bind:class="statusCssClass(batch.status)" v-bind:to="'/indicatorgroups/' + indicatorGroupId + '/batches/' + batch.id + '/logs'">
              {{ batch.status }}
            </router-link>
          </td>
          <td>
            {{ batch.sessionsByBatchId.totalCount }}
          </td>
          <td>
            <router-link class="badge badge-secondary" v-bind:to="'/indicatorgroups/' + indicatorGroupId + '/batches/' + batch.id + '/logs'">
              Log
            </router-link>
            <a v-if="showKillBatch(batch.status)" class="badge badge-secondary ml-1" v-on:click="setModalBoxBatchId(batch.id)" data-toggle="modal" data-target="#ModalBoxKillBatch">
              Kill
            </a>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal box to kill batch -->
    <modal-box-kill-batch v-bind:batchId="modalBoxBatchId"> </modal-box-kill-batch>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import ModalBoxKillBatch from "../utils/ModalBoxKillBatch.vue";

export default {
  mixins: [Mixins],
  components: {
    "modal-box-kill-batch": ModalBoxKillBatch
  },
  props: {
    indicatorGroupId: Number,
    batches: Array
  },
  data: function() {
    return {
      modalBoxBatchId: null
    };
  },
  computed: {
  },
  methods: {
    showKillBatch(batchStatus) {
      // Show kill batch
      let roles = ["standard", "advanced", "admin"];
      let status = ["Success", "Failed", "Killed"];
      return roles.includes(this.$store.state.currentUser.role) && !status.includes(batchStatus);
    },
    setModalBoxBatchId(batchId) {
      this.modalBoxBatchId = batchId;
    }
  }
};
</script>
