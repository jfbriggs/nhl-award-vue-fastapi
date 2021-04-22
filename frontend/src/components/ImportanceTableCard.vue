<template>
  <div class="container-fluid">
    <div class="card shadow-1-strong">
      <div class="card-header">
        <h6 class="pt-2">Model Feature Importance Values: Top 10</h6>
        <div><small>(Sorted, Descending)</small></div>
      </div>
      <div class="card-body">
        <table class="table table-sm">
          <thead>
            <tr>
              <th scope="col">Variable/Feature Name</th>
              <th scope="col">Importance Value</th>
            </tr>
          </thead>
          <tbody>
            <tr :key="name" v-for="(val, name) in featureImportances">
              <td>{{name}}</td>
              <td>{{val}}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer">
        <small>Feature importance values indicate how much predictive value/impact each feature/variable had in model training.</small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImportanceTableCard',
  props: {
    featureImportances: Object
  }
}
</script>

<style scoped>
.card-header {
  padding: .5rem 1rem .7rem 1rem;
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