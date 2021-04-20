<template>
  <div class="container">
    <div class="card shadow-1-strong card-list-header">
      <div class="card-header">
        <h4 class="pt-2">{{awardName}}</h4>
      </div>
      <div class="card-footer">
        <div class="col updated"><small>Data & Model Last Updated: {{dataUpdated}}</small></div>
      </div>
    </div>

    <div class="card shadow-1-strong card-list-header" v-show="!loading">
      <div class="card-body">
        <div class="col"><strong>Top 10: If the season were to end today...</strong></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AwardHeaderCard',
  props: {
    awardName: String,
    dataUpdated: String,
    loading: Boolean
  }
}
</script>

<style scoped>
.card-list-header {
  width: 50%;
  margin: 0 auto 10px auto;
  text-align: center;
}

.updated {
  color: rgb(105, 105, 105);
  font-style: italic;
}
</style>