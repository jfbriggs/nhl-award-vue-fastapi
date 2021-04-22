<template>
  <div class="container">
    <div class="card shadow-1-strong card-list-header">
      <div class="card-header">
        <h4 class="pt-2">{{awardName}}</h4>
      </div>
      <div class="card-body" id="top-header-body">
        <button
          type="button"
          class="btn btn-sm btn-light"
          data-mdb-toggle="modal"
          data-mdb-target="#awardModal"
        >
          Award/Model Info
        </button>
        <AwardModal :awardName="awardName" :featureImportances="featureImportances" />
      </div>
      <div class="card-footer">
        <div class="col updated"><small>Data & Model Last Updated: {{dataUpdated}}</small></div>
      </div>
    </div>

    <div class="card shadow-1-strong card-list-header" v-show="!loading">
      <div class="card-body">
        <div class="col"><strong>Current Predictions</strong></div>
      </div>
    </div>
  </div>
</template>

<script>
import AwardModal from '@/components/AwardModal'

export default {
  name: 'AwardHeaderCard',
  components: {
    AwardModal
  },
  props: {
    awardName: String,
    dataUpdated: String,
    loading: Boolean,
    featureImportances: Array
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

#top-header-body {
  padding: 0.6em;
}

</style>