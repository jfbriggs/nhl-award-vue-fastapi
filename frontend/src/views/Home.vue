<template>
  <div>
    <AwardHeaderCard awardName="James Norris Memorial Trophy" :dataUpdated="dataUpdated" :loading="loading" />
    <LoadingCard v-show="loading" />
    <PlayerCardList :data="predictionResults" />
  </div>
</template>

<script>
// @ is an alias to /src
import PlayerCardList from '@/components/PlayerCardList'
import LoadingCard from '@/components/LoadingCard'
import AwardHeaderCard from '@/components/AwardHeaderCard'

export default {
  name: 'Home',
  components: {
    PlayerCardList,
    LoadingCard, 
    AwardHeaderCard
  },
  data() {
    return {
      predictionResults: [],
      loading: true,
      dataUpdated: ""
    }
  },
  methods: {
    async getPredictions() {
      console.log("Gathering data...")
      const res = await fetch('http://localhost:8500/predict')
      const data = await res.json()
      const results = await data.results
      const updated = await data.updated

      let playerList = []

      for (const rank in results) {
        playerList.push({
          rank: rank,
          name: results[rank].name,
          team: results[rank].team,
          pointPct: results[rank].predicted_point_pct,
          teamLogo: results[rank].team_logo_url,
          headshot: results[rank].headshot_url,
          nhlPage: results[rank].nhl_page
        })
      }

      this.loading = false
      this.dataUpdated = updated
      return playerList

    }
  },
  async created() {
    this.predictionResults = await this.getPredictions()
  }
}
</script>
