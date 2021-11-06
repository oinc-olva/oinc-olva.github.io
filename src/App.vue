<template>
  <Header :socialLinks="socialLinks" />
  <Hero :latestVideos="latestVideos" />
  <router-view v-slot="{ Component }">
    <transition name="fade">
      <component :is="Component" :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" :channelUploads="videos" :latestVideos="latestVideos" :publishSchoolYears="publishSchoolYears" />
    </transition>
  </router-view>
  <Footer :socialLinks="socialLinks" />
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Footer
  },
  data() {
    return {
      videos: null,
      latestVideos: null,
      channelName: null,
      channelSubsFormatted: null,
      channelUploads: null,
      publishSchoolYears: null,
      socialLinks: null
    }
  },
  async created() {
    let channelData = await this.fetchChannelData()
    this.channelName = channelData.title
    this.videos = channelData.uploads.content
    this.publishSchoolYears = channelData.publishSchoolYears
    this.latestVideos = [];
    for (let year of this.publishSchoolYears) {
      let videos = this.videos[year]
      for (let i = 0; i < videos.length; i++) {
        this.latestVideos.push(videos[i]);
      }
    }

    this.channelSubsFormatted = channelData.statistics.subscriberCount
    if (this.channelSubsFormatted >= 1000000) { // Als ze boven de miljoen krijgen, dan snap ik er niets meer van
      this.channelSubsFormatted /= 1000000
      this.channelSubsFormatted += " mln."
    } else if (this.channelSubsFormatted >= 1000) { // Boven de duizend abonnementen kan nog eventueel
      this.channelSubsFormatted /= 1000
      this.channelSubsFormatted += " K"
    }

    this.socialLinks = channelData.socialLinks
  },
  methods: {
    async fetchChannelData() {
      const res = await fetch('/channeldata.json')
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
  .fade-leave-to {
    position: absolute;
    width: 100%;
    opacity: 0;
    transition: opacity .4s ease-in-out;
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
  button {
    border: none;
    border-radius: 2px;
    background-color: gray;
    color: white;
    padding: 10px 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color .1s ease-in-out;
    &:hover { background-color: rgb(104, 104, 104); }
}
</style>
