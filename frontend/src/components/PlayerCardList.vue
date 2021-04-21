<template>
    <div>
        <div class="container" :key="player.rank" v-for="player in data">
            <PlayerCard :playerData="player" />
        </div>
    </div>
</template>

<script>
import PlayerCard from '@/components/PlayerCard'

export default {
    name: 'PlayerCardList',
    components: {
        PlayerCard
    },
    props: {
        data: Array
    }
}
</script>

<style scoped>

</style>