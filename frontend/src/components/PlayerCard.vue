<template>
    <div class="card">
        <div class="card-header" @click="bodyShowing = !bodyShowing">
            <div class="media">
                <span class="badge badge-secondary align-self-center">{{playerData.rank}}</span>
                <a :href="playerData.nhlPage" target="_blank">
                    <img class="align-self-center mr-3 headshot rounded-circle" :src="playerData.headshot" alt="Headshot placeholder">
                </a>
                <div class="media-body">
                    <h5 class="mt-1">{{playerData.name}}</h5>
                </div>
                <img class="align-self-center mr-3 team-logo" :src="playerData.teamLogo" alt="Logo placeholder">
            </div>
        </div>
        <div class="card-body">
            <div class="col">Current Predicted Vote Point Percentage: {{playerData.pointPct}}%</div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PlayerCard',
    props: {
        playerData: Object
    },
    data() {
        return {
            bodyShowing: false
        }
    }
}
</script>

<style scoped>
.card {
    margin-top: 5px;
}

.headshot, .team-logo {
    height: 64px
}

.media-body {
    align-self: center;
}

.badge {
    margin-right: 10px;
}

</style>