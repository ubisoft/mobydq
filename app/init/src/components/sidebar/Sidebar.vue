<template>
  <nav id="sidebar" class="nav flex-column col sidebar">
    <span class="navbar-brand">
      <router-link to="/">
        <img src="logo.png"  alt="MobyDQ" />
      </router-link>
    </span>
    <a class="nav-link" href="#">Indicators</a>
    <a class="nav-link" href="#">Indicator Groups</a>
    <a class="nav-link active" href="#">Data Sources</a>    
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
