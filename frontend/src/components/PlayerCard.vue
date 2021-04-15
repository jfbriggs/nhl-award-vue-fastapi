<template>
    <div class="card">
        <div class="card-header" @click="bodyShowing = !bodyShowing">
            <div class="media">
                <a href="https://www.nhl.com/player/alex-ovechkin-8471214" target="_blank">
                    <img class="align-self-center mr-3 headshot rounded-circle" src="https://cms.nhl.bamgrid.com/images/headshots/current/168x168/8471214.jpg" alt="Headshot placeholder">
                </a>
                <div class="media-body">
                    <h5 class="mt-1">{{playerData.name}} <span class="badge badge-secondary">{{playerData.rank}}</span></h5>
                </div>
                <img class="align-self-center mr-3 team-logo" src="https://cdn.usteamcolors.com/images/nhl/washington-capitals.svg" alt="Logo placeholder">
            </div>
        </div>
        <div class="card-body" v-if="bodyShowing">
            <div class="col">Current Prediction Rank: {{playerData.rank}}</div>
            <div class="col">Predicted Vote Point Percentage: {{playerData.pointPct}}%</div>
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

.card-header {
    cursor: pointer;
}

.headshot, .team-logo {
    height: 64px
}

.media-body {
    align-self: center;
}

</style>