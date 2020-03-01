<template>
  <div class="mt-4">
    <table class="table table-striped table-dark table-hover table-borderless table-sm">
      <thead>
        <tr>
          <th scope="col">
            Session Id
          </th>
          <th scope="col">
            Status
          </th>
          <th scope="col">
            Nb Alerts
          </th>
          <th scope="col">
            Quality Level
          </th>
          <th scope="col">
            Batch Id
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
            <router-link class="badge badge-pill" v-bind:class="statusCssClass(session.status)" v-bind:to="'/indicators/' + indicatorId + '/sessions/' + session.id + '/logs'">
              {{ session.status }}
            </router-link>
          </td>
          <td>
            {{ session.nbRecordsAlert }}
          </td>
          <td v-if="session.nbRecords > 0">
            {{ Math.round((session.nbRecordsNoAlert/session.nbRecords)*100) }}%
          </td>
          <td v-else>
          </td>
          <td>
            <router-link v-bind:to="'/indicatorgroups/' + indicatorGroupId">
              {{ session.batchId }}
            </router-link>
          </td>
          <td>
            <router-link class="badge badge-secondary" v-bind:to="'/indicators/' + indicatorId + '/sessions/' + session.id + '/logs'">
              Log
            </router-link>
            <a v-if="showKillBatch(session.batchByBatchId.status)" class="badge badge-secondary ml-1" v-on:click="setModalBoxBatchId(session.batchId)" data-toggle="modal" data-target="#ModalBoxKillBatch">
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
    indicatorId: Number,
    indicatorGroupId: Number,
    sessions: Array
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
