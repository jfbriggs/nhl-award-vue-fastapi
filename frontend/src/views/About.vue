<template>
  <div class="about container content">
    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">About These Predictions</h5>
      </div>
      <div class="card-body">
        <div class="container">
          <p>Award voting outcome predictions are made using machine learning methods.</p>
          <p>Historical data that includes individual player stats, team standings performance, and past award voting outcomes (all on a per-season basis, sourced from <a href="https://www.hockey-reference.com/" target="_blank">hockey-reference.com)</a> is collected and processed. Subsequently, a regression model is fit using this data and used to make predictions based on the current season's data in an "if the season were to end today or current trends were to continue through to end-of-season, here is what the predicted outcome would be" manner.
          The data for each player involved includes that player's performance within a set of metrics/statistics relative to the rest of players in the league, the team they play for, and their team's performance in the standings relative to the rest of the league.</p>
          <p>The variable our models use to make predictions and rank players is "vote point percentage."  Currently: each season, every voter casts 1st through 5th place votes, each of which are worth a certain number of points (i.e. 10 for 1st, 7 for 2nd, 5 for 3rd, 3 for 4th, 1 for 5th). A player's total points is based on the sum of "vote points" they received from all voters, and final award placement is determined based on these totals.  As an additional step for predictive modeling, "vote point percentage" is then calculated as a player's total "vote points" received divided by the total "vote points" available based on all votes cast by all voters.</p>
          <p>As a penultimate step, predicted percentage values less than the lowest possible percentage value realistically achievable (e.g. roughly 0.023% for a single 5th place vote, in the case of the Norris Trophy, currently) are eliminated (converted to 0).</p>
          <p>Finally: because of the nature of the model's calculations and output (which tend to result in predicted values with sum >100%), exact output values are re-scaled to total 100%.</p>
          <p class="about-card-body">See <a href="https://nbviewer.jupyter.org/github/jfbriggs/nhl_norris_voting/blob/master/NorrisTrophyVoting.ipynb" target="_blank">this original project notebook file</a> for a full breakdown of the machine learning workflow involved in the data acquisition & preprocessing, model evaluation/selection, and prediction processes for the Norris Trophy at the end of the 2019-2020 season.</p>
        </div>
      </div>
    </div>

    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">Prediction/Machine Learning Caveats</h5>
      </div>
      <div class="card-body">
          <div class="container">
            <p>Machine learning, while a field that is continually advancing, is an inexact science.  Loosely speaking, it is a process meant to <i><strong>most closely approximate</strong></i> the relationship between some number of independent variables (i.e. various player stats, in our case) and a dependent variable (vote point percentage, in our case).</p>
            <p>While the data preparation and model selected for making these predictions have been established to perform quite well overall, the results are likely to never match actual outcomes exactly, especially given that these awards are based on votes cast by humans (meaning there are plenty of non-quantifiable variables that can impact voting decisions).</p>
            <p class="about-card-body">Outliers are always likely to exist, and there is always potential for modeling performance to be improved through various means.</p>
          </div>
      </div>
    </div>

    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">Why aren't there predictions for more awards?</h5>
      </div>
      <div class="card-body">
          <div class="container">
            <p>Working on it!  Predictions for other awards coming soon.</p>
            <p class="about-card-body">See the project notebook mentioned above for a sense of the process involved in determining what data to use, what steps to include to process it, and what model/parameters to select.</p>
          </div>
      </div>
    </div>

    <div class="card shadow-1-strong">
      <div class="card-header px-4 pt-3">
        <h5 class="about-title">Contact</h5>
      </div>
      <div class="card-body">
          <div class="container">
            <p class="about-card-body">For any inquiries, please e-mail <i>jfbriggs106</i> at <i>gmail</i> dot <i>com</i>.</p>
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