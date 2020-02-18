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
            <span class="badge badge-pill" v-bind:class="statusCssClass(session.status)" >
              {{ session.status }}
            </span>
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
            {{ session.batchId }}
          </td>
          <td>
            <router-link class="badge badge-secondary" v-bind:to="'/indicators/' + indicatorId + '/sessions/' + session.id + '/logs'">
              Log
            </router-link>
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
  components: {
  },
  props: {
    indicatorId: Number,
    sessions: Array
  },
  computed: {
  },
  methods: {
  }
};
</script>
