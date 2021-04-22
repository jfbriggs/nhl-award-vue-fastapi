<template>
    <div class="card shadow-1-strong">
        <div class="card-header">
            <div class="d-flex align-items-center p-2 pt-3">
                <div class="badge bg-dark flex-shrink-0">{{playerData.rank}}</div>
                <div class="flex-shrink-0 px-2">
                    <a :href="playerData.nhlPage" target="_blank" data-toggle="tooltip" data-placement="right" :title="'Visit ' + playerData.name + '\'s NHL.com page'">
                        <img class="align-self-center headshot rounded-circle" :src="playerData.headshot" alt="Headshot">
                    </a>
                </div>
                <div class="flex-grow-1 px-2">
                    <h5 class="card-title">{{playerData.name}}</h5>
                </div>
                <div class="flex-shrink-0">
                    <img class="mr-3 team-logo" :src="playerData.teamLogo" alt="Team Logo" data-toggle="tooltip" data-placement="right" :title="playerData.teamFullName">
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="col px-2">Current Predicted Vote Point Percentage: {{playerData.pointPct}}%</div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PlayerCard',
    props: {
        playerData: Object
    }
}
</script>

<style scoped>
.card {
    width: 98%;
    margin: 8px auto;
}

.card:hover {
    box-shadow: 2em;
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