<template>
  <Header />
  <Hero :latestVideos="latestVideos" />
  <router-view :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero
  },
  data() {
    return {
      videos: [],
      latestVideos: [],
      channelName: null,
      channelSubsFormatted: null
    }
  },
  async created() {
    let channelData = await this.fetchChannelData()
    this.videos = channelData.uploads.content
    this.latestVideos = this.videos.slice(0, 5)
    this.channelName = channelData.title

    this.channelSubsFormatted = channelData.statistics.subscriberCount
    if (this.channelSubsFormatted >= 1000000) { // Als ze boven de miljoen krijgen, dan snap ik er niets meer van
      this.channelSubsFormatted /= 1000000
      this.channelSubsFormatted += " mln."
    } else if (this.channelSubsFormatted >= 1000) { // Boven de duizend abonnementen kan nog eventueel
      this.channelSubsFormatted /= 1000
      this.channelSubsFormatted += " K"
    }
  },
  methods: {
    async fetchChannelData() {
      const res = await fetch('channeldata.json')
      const data = await res.json()
      return data
    },
  }
}
</script>


<style lang="scss">
  @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

  * {
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
  }
  body {
    background-color: black;
    overflow-y: scroll;
  }
  .container {
    width: calc(100vw - 40%);
    margin: 0 auto;
  }
  a {
    position: relative;
    text-decoration: none;
    cursor: pointer;

    &::before {
      content: '';
      display: inline-block;
      position: absolute;
      bottom: 0; left: 0;
      height: 1px;
      width: 0;
      background-color: white;
      transition: width .2s ease-in-out;
    }
    &:hover::before { width: 100%; }
  }
</style>
