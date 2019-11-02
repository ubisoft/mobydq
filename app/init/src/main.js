import Vue from "vue";
import VueResource from "vue-resource";
import VueRouter from "vue-router";
import VueSession from "vue-session";
import App from "./App.vue";
import { store } from "./store";

// Custom components
import Login from "./components/Login.vue";
import EditUser from "./components/EditUser.vue";
import EditUserGroup from "./components/EditUserGroup.vue";
import ViewUser from "./components/ViewUser.vue";
import ViewUserGroup from "./components/ViewUserGroup.vue";

// Tell Vue to use libraries
Vue.use(VueResource);
Vue.use(VueRouter);
Vue.use(VueSession, { persist: true });

// Declare application URLs
const routes = [
  { name: "home", path: "/", component: ViewUser },
  { name: "login", path: "/login", component: Login },
  { name: "view-user", path: "/admin/users", component: ViewUser },
  { name: "edit-user", path: "/admin/users/:userId", component: EditUser },
  { name: "view-user-group", path: "/admin/usergroups", component: ViewUserGroup },
  { name: "edit-user-group", path: "/admin/usergroups/:userGroupId", component: EditUserGroup }
];

// Configure router
const router = new VueRouter({
  routes,
  mode: "history"
});

Vue.config.productionTip = false; // Not sure what this is for
// Create Vue instance
new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App)
}).$mount("#app");
