<template>
  <div>
    <PlayerCardList :data="predictionResults" />
  </div>
</template>

<script>
// @ is an alias to /src
import PlayerCardList from '@/components/PlayerCardList'

export default {
  name: 'Home',
  components: {
    PlayerCardList
  },
  data() {
    return {
      predictionResults: []
    }
  },
  methods: {
    async getPredictions() {
      console.log("Gathering data...")
      const res = await fetch('http://localhost:8500/predict')
      const data = await res.json()
      const results = await data.results

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

      return playerList

    }
  },
  async created() {
    this.predictionResults = await this.getPredictions()
  }
}
</script>
