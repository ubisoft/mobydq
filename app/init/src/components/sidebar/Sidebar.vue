<template>
  <div id="sidebar">
    <span class="navbar-brand">
      <router-link to="/">
        <img src="/logo.png"  alt="MobyDQ" />
      </router-link>
    </span>

    <!-- Menu -->
    <router-link to="/" class="nav-link">
      Dashboard
    </router-link>
    <router-link to="/indicators" class="nav-link">
      Indicators
    </router-link>
    <router-link to="/indicatorgroups" class="nav-link">
      Indicator Groups
    </router-link>
    <router-link to="/datasources" class="nav-link">
      Data Sources
    </router-link>
  </div>
</template>

<script>
</script>

<style>
#sidebar {
  height: 100%;
  width: 250px;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #212529;
  overflow-x: hidden;
  padding-top: 20px;
}

.nav-link {
  color: #cccccc;
  padding-top: 10px;
  padding-bottom: 10px;
}

.nav-link:hover {
  color: #ffffff;
}
</style>