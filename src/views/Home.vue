<template>
  <div class="home">
    <Homevideoslides :videos="latestvideos" />
  </div>
</template>

<script>
import Homevideoslides from '../components/Homevideoslides.vue'
export default {
  components: { Homevideoslides },
  data() {
    return {
        latestvideos: []
    }
  },
  async created() {
    this.latestvideos = await this.fetchLatestThreeVideos()
  },
  methods: {
    async fetchLatestThreeVideos() {
      const res = await fetch('channeldata.json')
      const data = await res.json()
      return data.uploads.content.slice(0, 5)
    }
  }
}
</script>

<style lang="scss" scoped>
</style>