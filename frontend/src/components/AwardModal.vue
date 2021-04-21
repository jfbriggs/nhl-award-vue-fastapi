<template>
  <!-- Modal -->
  <div
    class="modal fade"
    id="awardModal"
    tabindex="-1"
    aria-labelledby="awardModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="awardModalLabel">Award Information</h5>
          <button
            type="button"
            class="btn-close"
            data-mdb-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">Hello there!</div>
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
export default {
  name: 'AwardModal',
  props: {
    awardName: String
  }
}
</script>

<style scoped>

</style>