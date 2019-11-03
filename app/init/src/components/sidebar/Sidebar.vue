<template>
  <nav id="sidebar" class="nav flex-column col sidebar">
    <span class="navbar-brand">
      <router-link to="/">
        <img src="logo.png"  alt="MobyDQ" />
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
  </nav>
</template>

<script>
</script>

<style>
.navbar-brand {
  margin-bottom: 20px;
}

.sidebar {
  background-color: #212529;
  min-width: 250px;
  max-width: 250px;
  min-height: 100vh;
  padding: 0;
}

a.nav-link {
  color: #cccccc;
  padding-top: 10px;
  padding-bottom: 10px;
}

a.nav-link:hover {
  color: #ffffff;
}

a.nav-link.active {
  min-width: 250px;
  max-width: 250px;
  background-color: #2c3034;
}
</style>
