<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless">
      <thead>
        <tr>
          <th scope="col">
            Session Id
            <table-sort v-bind:columnName="'id'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Indicator Name
          </th>
          <th scope="col">
            Session Status
            <table-sort v-bind:columnName="'STATUS'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Updated Date
            <table-sort v-bind:columnName="'UPDATED_DATE'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Created By
          </th>
          <th scope="col">
            Batch Id
            <table-sort v-bind:columnName="'BATCH_ID'" v-bind:sortAttribute="sortAttribute" v-on:sortAttribute="setSortAttribute"></table-sort>
          </th>
          <th scope="col">
            Batch Status
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
            <router-link v-bind:to="'/indicators/' + session.indicatorId">
              {{ session.indicatorByIndicatorId.name }}
            </router-link>
          </td>
          <td>
            <router-link class="badge badge-pill" v-bind:class="statusCssClass(session.status)" v-bind:to="'/indicators/' + session.indicatorId">
              {{ session.status }}
            </router-link>
          </td>
          <td>
            {{ session.updatedDate }}
          </td>
          <td>
            {{ session.userByCreatedById.email }}
          </td>
          <td>
            {{ session.batchId }}
          </td>
          <td>
            <router-link class="badge badge-pill" v-bind:class="statusCssClass(session.batchByBatchId.status)" v-bind:to="'/indicatorGroups/' + session.batchByBatchId.indicatorGroupId">
              {{ session.batchByBatchId.status }}
            </router-link>
          </td>
          <td>
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
import TableSort from "../utils/TableSort.vue";
import ModalBoxKillBatch from "../utils/ModalBoxKillBatch.vue";

export default {
  mixins: [Mixins],
  components: {
    "table-sort": TableSort,
    "modal-box-kill-batch": ModalBoxKillBatch
  },
  props: {
    sessions: Array,
    sortAttribute: Object
  },
  data: function() {
    return {
      modalBoxBatchId: null
    };
  },
  computed: {
  },
  methods: {
    setSortAttribute(attribute) {
      this.$emit("sortAttribute", attribute);
    },
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
