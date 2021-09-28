<template>
  <div class="home">
    <Videoslideshow :videos="latestvideos" />
  </div>
</template>

<script>
import Videoslideshow from '../components/Videoslideshow.vue'
export default {
  components: { Videoslideshow },
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
            return data.uploads.content.slice(0, 3)
        }
  }
}
</script>

<style lang="scss" scoped>
  .home {
    padding-top: 60px;
  }
</style>