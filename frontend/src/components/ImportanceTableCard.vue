<template>
  <div class="container-fluid">
    <div class="card shadow-1-strong">
      <div class="card-header" data-toggle="tooltip" data-placement="bottom" :title="importanceTooltip">
        <h6 class="pt-2">Model Feature Importance Values: Top 10</h6>
        <div><small>(Sorted, Descending)</small></div>
      </div>
      <div class="card-body">
        <table class="table">
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
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImportanceTableCard',
  props: {
    featureImportances: Array
  },
  data() {
    return {
      importanceTooltip: "Feature importance values indicate how much predictive value each feature/variable had in model fitting."
    }
  }
}
</script>

<style scoped>
h6 {
  margin-bottom: 0;
}
</style>