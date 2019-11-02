<template>
  <div v-if="show" class="dropdown">
    <button class="btn btn-secondary dropdown-toggle ml-1" id="admin" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
      Admin
    </button>
    <div class="dropdown-menu dropdown-menu-lg-right" aria-labelledby="admin">
      <router-link to="/admin/users" class="dropdown-item">
        Users
      </router-link>
      <router-link to="/admin/usergroups" class="dropdown-item">
        User Groups
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    show() {
      let roles = ["admin"];
      return roles.includes(this.$store.state.currentUser.role);
    }
  }
};
</script>
