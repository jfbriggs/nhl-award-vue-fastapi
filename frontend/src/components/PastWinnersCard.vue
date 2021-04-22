<template>
  <div class="container-fluid">
    <div class="card shadow-1-strong">
      <div class="card-header">
        <h6 class="pt-2">Past Winners</h6>
      </div>
      <div class="card-body overflow-auto">
        <table class="table table-sm">
          <thead>
            <tr>
              <th scope="col">Season</th>
              <th scope="col">Player</th>
              <th scope="col">Team</th>
            </tr>
          </thead>
          <tbody>
            <tr :key="winner[0]" v-for="winner in pastWinners">
              <td>{{winner[0]}}</td>
              <td>{{winner[1]}}</td>
              <td>{{winner[2]}}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        <small>Award winners since award was introduced to the league.</small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PastWinnersCard',
  props: {
    pastWinners: Array
  }
}
</script>

<style scoped>
.container-fluid {
  margin-top: 10px;
}

.card-body {
  max-height: 35rem;
}

.card-header {
  padding: .5rem 1rem 1rem 1rem;
}

h6 {
  margin-bottom: 0;
}

.card-footer {
  color: rgb(167, 167, 167);
}

.card-footer:hover {
  color: black;
}
</style>