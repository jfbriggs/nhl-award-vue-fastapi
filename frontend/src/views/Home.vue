<template>
  <div>
    <AwardHeaderCard awardName="James Norris Memorial Trophy" :dataUpdated="dataUpdated" :loading="loading" :featureImportances="featureImportances" :pastWinners="pastWinners"/>
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
      featureImportances: {},
      pastWinners: [],
      loading: true,
      dataUpdated: ""
    }
  },
  methods: {
    async getPredictions() {
      const res = await fetch('http://' + window.location.host + ':8500/predict')
      const data = await res.json()
      const results = await data.results
      const updated = await data.updated
      const featureImportances = await data.importances
      const pastWinners = await data.past_winners

      let playerList = []

      for (const rank in results) {
        playerList.push({
          rank: rank,
          name: results[rank].name,
          team: results[rank].team,
          teamFullName: results[rank].team_full,
          pointPct: results[rank].predicted_point_pct,
          teamLogo: results[rank].team_logo_url,
          headshot: results[rank].headshot_url,
          nhlPage: results[rank].nhl_page
        })
      }

      this.loading = false
      this.dataUpdated = updated
      this.featureImportances = featureImportances
      this.pastWinners = pastWinners
      return playerList

    }
  },
  async created() {
    this.predictionResults = await this.getPredictions()
  }
}
</script>
