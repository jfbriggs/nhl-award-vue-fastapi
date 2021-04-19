<template>
  <div class="about container content">
    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">About These Predictions</h5>
      </div>
      <div class="card-body">
        <div class="container">
          <p>These predictions are made using machine learning methods.</p>
          <p>Historical data (starting with the 1979-1980 season) that includes individual player stats, team standings performance, and Norris Trophy voting outcomes; is collected and prepared. Subsequently, a gradient boosting regression model is fit using this data and used to make predictions based on the current season's data in an "if the season were to end today, here is what the predicted outcome would be" manner.</p>
          <p>Voting percentage is calculated as a proportion of total available vote points. Currently: each season, every voter casts 1st through 5th place votes, each of which are worth a certain number of points (i.e. 9 for 1st, 7 for 2nd, 5 for 3rd, 3 for 4th, 1 for 5th). A player's total points is based on the sum of "vote points" they received from all voters, and final award placement is determined based on these totals. For the sake of this model, "vote point percentage" is calculated as the total "vote points" received divded by the total "vote points" available based on all votes cast by all voters.</p>
          <p class="about-card-body">See <a href="https://nbviewer.jupyter.org/github/jfbriggs/nhl_norris_voting/blob/master/NorrisTrophyVoting.ipynb" target="_blank">this original project notebook file</a> for a full breakdown of the machine learning workflow involved in the data acquisition & preprocessing, model evaluation/selection, and prediction processes.</p>
        </div>
      </div>
    </div>

    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">Other Awards</h5>
      </div>
      <div class="card-body">
          <div class="container">
            <p class="about-card-body">Predictions for other awards coming soon!</p>
          </div>
      </div>
    </div>

    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">Contact</h5>
      </div>
      <div class="card-body">
          <div class="container">
            <p class="about-card-body">For any inquiries, please e-mail <i>jfbriggs106</i> at <i>gmail</i> dot <i>com</i></p>
          </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
a {
  color: rgb(77, 77, 255);
}

.about-title {
  margin-left: 5px;
}

.card:not(:first-child) {
    margin-top: 8px;
}

.about-card-body {
  margin: 0;
}
</style>