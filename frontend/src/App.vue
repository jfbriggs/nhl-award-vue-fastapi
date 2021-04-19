<template>
  <div>
    <!-- Nav bar -->
    <nav class="navbar navbar-dark bg-dark sticky-top">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand px-2">NHL Award Prediction Tracker</router-link>
        <ul class="nav justify-content-center">
          <li class="nav-item">
            <router-link to="/" class="nav-link active" href="#">HOME</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link" href="#">ABOUT</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Container for rest of page, router views -->
    <div class="content">
      <router-view />
    </div>
    <div class="container-fluid text-center footer">Made with &#10084; by <a href="https://github.com/jfbriggs" target="_blank" id="github">JFB</a>.</div>
  </div>
</template>

<script>
export default {
  title: 'NHL Award Predictions',
  components: {
  },
  created() {
    document.title = 'NHL Award Prediction Tracker'
  }
}
</script>

<style>
body {
  background-color: #f7f7f7;
}

a {
  color: #9c9c9c
}

a:hover {
  color: white;
}

#github:hover {
  color: #4d4d4d
}

.footer {
  background-color: #fff;
  margin-top: 25px;
  border-top: 1px solid rgba(0,0,0,.12);
  padding: 10px 0;
  height: auto;
}

.content {
  padding-top: 10px;
}
</style>
