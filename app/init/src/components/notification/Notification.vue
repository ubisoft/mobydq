<template>
  <div>
    <notificatio-button-mar-all-read
      v-if="show"
      v-on:markAllNotificationsAsRead="getAllNotifications"
    >
    </notificatio-button-mar-all-read>
    
    <notification-table
      v-bind:notifications="notifications"
      v-on:markAllNotificationsAsRead="getAllNotifications"
      v-on:markNotificationAsRead="removeNotification"
    >
    </notification-table>
  </div>
</template>

<script>
import Mixins from "../utils/Mixins.vue";
import NotificationButtonMarkAllRead from "./NotificationButtonMarkAllRead.vue";
import NotificationTable from "./NotificationTable.vue";

export default {
  mixins: [Mixins],
  components: {
    "notificatio-button-mar-all-read": NotificationButtonMarkAllRead,
    "notification-table": NotificationTable
  },
  data: function() {
    return {
      notifications: []
    };
  },
  computed: {
    show() {
      return this.notifications.length > 0;
    }
  },
  methods: {
    getAllNotifications() {
      let payload = {
        query: this.$store.state.queryGetAllNotifications,
        variables: {
          orderBy: ["CREATED_DATE_DESC"]
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
            this.notifications = response.data.data.allNotifications.nodes;
          }
        },
        // Error callback
        function(response) {
          this.displayError(response);
        }
      );
    },
    removeNotification(value) {
      // Function to remove notification from table when it is mark as read
      this.notifications = this.notifications.filter(
        function(item) {
          return item.id != value;
        }
      );
    }
  },
  created: function() {
    this.getAllNotifications();
  }
};
</script>