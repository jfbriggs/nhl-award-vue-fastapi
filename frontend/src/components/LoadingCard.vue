<template>
  <div class="container">
      <div class="card shadow-1-strong">
        <div class="card-body text-center">
          <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'LoadingCard'
}
</script>

<style scoped>

.card {
  margin: 0 auto 10px auto;
  max-width: 650px;
}

</style>