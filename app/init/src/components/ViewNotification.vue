<template>
  <div class="col">
    <h1 class="mt-5">Notifications</h1>
    <notification></notification>
  </div>
</template>

<script>
import notification from "./notification/Notification.vue";

export default {
  components: {
    "notification": notification
  }
};
</script>
