import Vue from "vue";
import VueResource from "vue-resource";
import VueRouter from "vue-router";
import VueSession from "vue-session";
import VueNativeSock from "vue-native-websocket";

import App from "./App.vue";
import { store } from "./store";

// Custom components
import Login from "./components/Login.vue";
import EditUser from "./components/EditUser.vue";
import EditUserGroup from "./components/EditUserGroup.vue";
import EditDataSource from "./components/EditDataSource.vue";
import EditIndicatorGroup from "./components/EditIndicatorGroup.vue";
import EditIndicator from "./components/EditIndicator.vue";
import ViewDashboard from "./components/ViewDashboard.vue";
import ViewUser from "./components/ViewUser.vue";
import ViewUserGroup from "./components/ViewUserGroup.vue";
import ViewDataSource from "./components/ViewDataSource.vue";
import ViewIndicatorGroup from "./components/ViewIndicatorGroup.vue";
import ViewIndicator from "./components/ViewIndicator.vue";
import ViewLog from "./components/ViewLog.vue";
import ViewNotification from "./components/ViewNotification.vue";

// Tell Vue to use libraries
Vue.use(VueResource);
Vue.use(VueRouter);
Vue.use(VueSession, { persist: true });
Vue.use(VueNativeSock, "wss://" + window.location.host + "/graphql", {
  protocol: "graphql-ws",
  store: store,
  format: "json",
  reconnection: true, // Boolean to reconnect automatically
  reconnectionAttempts: 5, // Number of reconnection attempts before giving up
  reconnectionDelay: 3000 // How long to initially wait before attempting a new connection
});

// Declare application URLs
const routes = [
  { name: "home", path: "/", component: ViewDashboard },
  { name: "login", path: "/login", component: Login },
  { name: "view-user", path: "/admin/users", component: ViewUser },
  { name: "edit-user", path: "/admin/users/:userId", component: EditUser },
  { name: "view-user-group", path: "/admin/usergroups", component: ViewUserGroup },
  { name: "edit-user-group", path: "/admin/usergroups/:userGroupId", component: EditUserGroup },
  { name: "view-data-source", path: "/datasources", component: ViewDataSource },
  { name: "edit-data-source", path: "/datasources/:dataSourceId", component: EditDataSource },
  { name: "view-indicator-group", path: "/indicatorgroups", component: ViewIndicatorGroup },
  { name: "edit-indicator-group", path: "/indicatorgroups/:indicatorGroupId", component: EditIndicatorGroup },
  { name: "view-indicator", path: "/indicators", component: ViewIndicator },
  { name: "edit-indicator", path: "/indicators/:indicatorId", component: EditIndicator },
  { name: "view-batch-log", path: "/indicatorgroups/:indicatorGroupId/batches/:batchId/logs", component: ViewLog },
  { name: "view-session-log", path: "/indicators/:indicatorId/sessions/:sessionId/logs", component: ViewLog },
  { name: "view-data-source-log", path: "/datasources/:dataSourceId/logs", component: ViewLog },
  { name: "view-notification", path: "/notifications", component: ViewNotification }
];

// Configure router
const router = new VueRouter({
  routes,
  mode: "hash"
});

Vue.config.productionTip = false; // Not sure what this is for
// Create Vue instance
new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App)
}).$mount("#app");
