<template>
  <div>
    <table class="table table-striped table-dark table-hover table-borderless mt-5">
      <thead>
        <tr>
          <th scope="col">
            Message
          </th>
          <th scope="col">
            Created Date
          </th>
          <th scope="col">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="notification in notifications" v-bind:key="notification.id">
          <td>
            <!-- Batch notification -->
            <span  v-if="notification.batchId">
              Status of batch Id <b>{{ notification.batchId }}</b> set to
            </span>
            <!-- Data source notification -->
            <span  v-if="notification.dataSourceId">
              Status of data source <b>{{ notification.dataSourceByDataSourceId.name }}</b> set to
            </span>
            <span class="badge badge-pill" v-bind:class="statusCssClass(notification.status)">
              {{ notification.status }}
            </span>
          </td>
          <td>
            {{ notification.createdDate }}
          </td>
          <td>
            <a class="badge badge-secondary ml-1" v-on:click="markNotificationAsRead(notification.id)">
              Mark as read
            </a>
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
    notifications: Array
  },
  computed: {
  },
  methods: {
    markNotificationAsRead(notificationId) {
      let payload = {
        query: this.$store.state.mutationMarkNotificationsAsRead,
        variables: {
          id: notificationId
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
            this.$emit("markNotificationAsRead", notificationId);
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    }
  },
  created: function() {
    // Capture notification via websocket listener
    this.$options.sockets.onmessage = function(data) {
      let message = JSON.parse(data.data);
      if (message.id == "notification" && message.type == "data") {
        this.notifications.unshift(message.payload.data.listen.relatedNode); // Push notification to array
      }
    };
  }
};
</script>
