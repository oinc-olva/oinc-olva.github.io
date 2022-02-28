<template>
  <div id="appWrapper" :class="{burgerMenuOpen: isBurgerMenuOpen}">
    <Header :socialLinks="socialLinks" :isBurgerMenuOpen="isBurgerMenuOpen" @toggleBurgerMenu="toggleBurgerMenu" />
    <Hero :latestVideos="latestVideos" />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="in-out">
        <component :is="Component" :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" :channelUploads="videos" :recommendedVideos="recommendedVideos" :playerVideo="playerVideo" :publishSchoolYears="publishSchoolYears" :aboutDesc="aboutDesc" />
      </transition>
    </router-view>
    <VideoPlayer v-show="!isBurgerMenuOpen" v-if="playerVideo" :video="playerVideo" :isOnVideoPage="isOnVideoPage" @close="closePlayer" />
    <Footer :socialLinks="socialLinks" />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Footer from './components/Footer.vue'
import VideoPlayer from './components/VideoPlayer.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Footer,
    VideoPlayer
  },
  data() {
    return {
      videos: null,
      latestVideos: null,
      recommendedVideos: null,
      playerVideo: null,
      channelName: null,
      channelSubsFormatted: null,
      publishSchoolYears: null,
      socialLinks: null,
      aboutDesc: null,
      isOnVideoPage: null,
      isBurgerMenuOpen: false
    }
  },
  async created() {
    let channelData = await this.fetchChannelData()
    this.channelName = channelData.title
    this.videos = channelData.uploadedVideos
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
    this.aboutDesc = channelData.description
    this.updateVideoInfo();

    // Zorg dat het burgermenu sluit als het scherm te breed wordt
    window.addEventListener('resize', () => {
      if (window.innerWidth > 480) this.isBurgerMenuOpen = false;
    });
  },
  methods: {
    async fetchChannelData() {
      const res = await fetch('/channeldata.json')
      const data = await res.json()
      return data
    },
    shuffle(arr) {
      // Fisher-Yates / Knuth Shuffle
      let currentIndex = arr.length, randomIndex;
      while (currentIndex != 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [arr[currentIndex], arr[randomIndex]] = [
          arr[randomIndex], arr[currentIndex]];
      }
      return arr;
    },
    mergeArrays(arr) {
      return Array.from(new Set([].concat(...arr)));
    },
    pickRandom(arr, n) {
      let randNumberArr = [...Array(arr.length).keys()];
      let randArr = [];
      this.shuffle(randNumberArr);
      for (let i = 0; i < n; i++) randArr.push(arr[randNumberArr[i]]);
      return randArr;
    },
    findNearbyVideos(latestVideoIndex, range) {
      let start = latestVideoIndex - range;
      if (start < 0) start = 0;
      let end = latestVideoIndex + range;
      if (end > this.latestVideos.length - 1) end = this.latestVideos.length - 1;
      
      let indexArr = this.latestVideos.slice();
      indexArr.splice(latestVideoIndex, 1);
      indexArr = indexArr.slice(start, end);
      this.shuffle(indexArr);
      return indexArr;
    },
    updateRecommendedVideos(latestVideoIndex) {
      this.recommendedVideos = this.mergeArrays([
        this.findNearbyVideos(latestVideoIndex, 2), // Suggereer een mix van video's die rond dezelfde datum zijn geüpload
        this.latestVideos.slice(0, 2), // Suggereer enkele nieuwste video's
        this.pickRandom(this.latestVideos, 4) // Suggereer willekeurige video's
      ]).filter((video) => video.id != this.playerVideo.id);
    },
    updateVideoInfo() {
      if (this.videos && this.$route.name == 'Video') {
        let latestVideoIndex = this.getLatestVideoIndex(this.$route.params.videoId);
        this.playerVideo = this.latestVideos[latestVideoIndex];
        this.updateRecommendedVideos(latestVideoIndex);
        this.isOnVideoPage = true;
      } else {
        this.isOnVideoPage = false;
      }
    },
    closePlayer() {
      this.playerVideo = null;
    },
    getLatestVideoIndex(id) {
      for (let i = 0; i < this.latestVideos.length; i++)
        if (this.latestVideos[i].id == id) return i;
    },
    closePlayer() {
      this.playerVideo = null;
    },
    toggleBurgerMenu() {
      this.isBurgerMenuOpen = !this.isBurgerMenuOpen;
    }
  },
  watch: {
    $route() {
      this.updateVideoInfo();
    }
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
    overflow-x: hidden;
    overflow-y: scroll;
  }
  .fade-leave-active {
    position: absolute;
    width: 100%;
    opacity: 0;
    z-index: 7;
    transition: opacity .6s ease-in-out;
  }
  .container {
    width: calc(100vw * #{1 - $containerMarginFrac});
    margin: 0 auto;
  }
  a {
    position: relative;
    text-decoration: none;
    color: rgb(170, 170, 170);
    cursor: pointer;

    &.link::before {
      content: '';
      display: inline-block;
      position: absolute;
      bottom: 0; left: 0;
      height: 1px;
      width: 0;
      background-color: rgb(170, 170, 170);
      transition: width .2s ease-in-out;
    }
    &.link:hover::before { width: 100%; }
  }
  button.btn {
    border: none;
    border-radius: 2px;
    background-color: #4a4e69;
    border: 2px solid transparent;
    color: rgb(221, 221, 221);
    padding: 10px 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color .2s ease-in-out,
                border-color .2s ease-in-out,
                color .4s ease-in-out;
    &:hover {
      background-color: #41455f;
      border-color: rgba(0, 0, 0, .1);
      color: rgb(216, 216, 216);
    }
  }
  button.icon {
    background-color: transparent;
    color: white;
    font-size: 20px;
    border: none;
    cursor: pointer;
  }

  #appWrapper.burgerMenuOpen {
    .view, .hero, .footer {
      filter: blur(10px);
    }
  }
</style>
