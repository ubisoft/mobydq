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
            <span class="badge badge-pill" v-bind:class="statusCssClass(batch.status)" >
              {{ batch.status }}
            </span>
          </td>
          <td>
            {{ batch.sessionsByBatchId.totalCount }}
          </td>
          <td>
            <router-link class="badge badge-secondary" v-bind:to="'/indicatorgroups/' + indicatorGroupId + '/batches/' + batch.id + '/logs'">
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
    indicatorGroupId: Number,
    batches: Array
  },
  computed: {
  },
  methods: {
  }
};
</script>
