<template>
  <div class="home">
    <h1>Home!</h1>
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
            return data.uploads.content
        }
  }
}
</script>