<template>
  <div>
    <!-- Nav bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand px-2">NHL Award Prediction Tracker</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-mdb-toggle="collapse"
          data-mdb-target="#navbarTogglerDemo02"
          aria-controls="navbarTogglerDemo02"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse justify-content-end px-2" id="navbarTogglerDemo02">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link" href="#">HOME</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link" href="#">ABOUT</router-link>
            </li>
          </ul>
        </div>
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
    console.log("Hi there!  Thanks for visiting.  Looks like you might be checking out my work on this app.  I'm currently looking for a job opportunity in data science, ML engineering, or SWE; so feel free to get in touch if you've got something in mind!")
    console.log("If you're interested in the repo for all of this app's code (including the underlying data preprocessing and ML), you can find it here: https://github.com/jfbriggs/nhl-award-vue-fastapi")
    console.log("The original Jupyter notebook ML project that this app is based on can also be found here: https://nbviewer.jupyter.org/github/jfbriggs/nhl_norris_voting/blob/master/NorrisTrophyVoting.ipynb")
    console.log("If you'd like to get in touch with me, my e-mail address is available in the 'About' view.")
  }
}
</script>

<style>
body {
  background-color: #f7f7f7;
}

.navbar-brand {
  font-family: 'Titillium Web', 'Roboto', sans-serif;
  font-weight: bold;
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
