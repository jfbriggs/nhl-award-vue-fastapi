<template>
  <div class="container">
      <div class="card shadow-1-strong">
        <div class="card-body text-center">
          <div class="spinner-border" role="status">
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
margin-bottom: 10px
}

</style>