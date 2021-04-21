<template>
  <!-- Modal -->
  <div
    class="modal fade"
    id="awardModal"
    tabindex="-1"
    aria-labelledby="awardModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="awardModalLabel">Award/Model Information</h5>
          <button
            type="button"
            class="btn-close"
            data-mdb-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <ImportanceTableCard :featureImportances="featureImportances" />
        </div>
        <div class="modal-footer justify-content-center">
          <div>
            <span><small>{{awardName}}</small></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImportanceTableCard from '@/components/ImportanceTableCard'

export default {
  name: 'AwardModal',
  components: {
    ImportanceTableCard
  },
  props: {
    awardName: String,
    featureImportances: Array
  }
}
</script>

<style scoped>

.modal-header {
  padding-left: 2em;
}

.modal-footer{
  padding: 0;
  opacity: 60%;
}
</style>