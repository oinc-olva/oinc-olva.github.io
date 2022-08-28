<template>
  <div id="appWrapper" :class="{burgerMenuOpen: isBurgerMenuOpen}">
    <CookieBanner v-if="isCookieBannerOpen" @confirm="confirmCookies" />
    <Header :socialLinks="socialLinks" :isBurgerMenuOpen="isBurgerMenuOpen" @toggleBurgerMenu="toggleBurgerMenu" />
    <MiniPlayer v-show="!isBurgerMenuOpen" v-if="playerVideo" :videos="videos" :playlists="playlists" :playerVideo="playerVideo" :recommendedVideoIds="recommendedVideoIds" :isAutoplay="isAutoplay" :isOnVideoPage="isOnVideoPage" @setCurrentVideoId="setCurrentVideoId" @close="closePlayer" />
    <main>
      <Hero :latestVideos="latestVideos" />
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="in-out">
          <component :is="Component" :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" :aboutDesc="aboutDesc" :videos="videos" :recommendedVideoIds="recommendedVideoIds" :playlists="playlists" :schoolYears="schoolYears" :playerVideo="playerVideo" :isAutoplay="isAutoplay" @setAutoplay="isAutoplay => this.isAutoplay = isAutoplay" />
        </transition>
      </router-view>
    </main>
    <Footer :socialLinks="socialLinks" />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Footer from './components/Footer.vue'
import CookieBanner from './components/CookieBanner.vue'
import MiniPlayer from './components/video/MiniPlayer.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Footer,
    CookieBanner,
    MiniPlayer
  },
  data() {
    return {
      videos: null,
      latestVideos: null,
      recommendedVideoIds: null,
      playlists: null,
      schoolYears: null,
      playerVideo: null,
      isAutoplay: true,
      channelName: null,
      channelSubsFormatted: null,
      socialLinks: null,
      aboutDesc: null,
      isOnVideoPage: null,
      isBurgerMenuOpen: false,
      isCookieBannerOpen: !this.getCookie('cookiesAccepted')
    }
  },
  async created() {
    let channelData = await this.fetchChannelData()
    this.channelName = channelData.title
    this.videos = channelData.videos
    this.playlists = channelData.playlists
    this.schoolYears = channelData.schoolYears

    this.latestVideos = (() => { // Vind de vier nieuwste video's
      let latestVideos = [];
      for (let videoId of this.videos.order) {
        latestVideos.push(this.videos.values[videoId]);
        if (latestVideos.length == 4) return latestVideos;
      }
      return latestVideos;
    })();

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
    this.testPageForVideo();

    // Zorg dat het burgermenu sluit als het scherm te breed wordt
    window.addEventListener('resize', () => {
      if (window.innerWidth > 480) this.isBurgerMenuOpen = false;
    });

    // Laad Analytics script
    if (this.getCookie('cookiesAccepted')) this.setAnalyticsScript();
  },
  methods: {
    async fetchChannelData() {
      const res = await fetch('/generated/data/channeldata.json')
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
    findNearbyVideos(videoIndex, range) {
      let start = videoIndex - range;
      if (start < 0) start = 0;
      let end = videoIndex + range;
      if (end > this.videos.order.length - 1) end = this.videos.order.length - 1;
      
      let videoIdArr = this.videos.order.slice();
      videoIdArr.splice(videoIndex, 1);
      videoIdArr = videoIdArr.slice(start, end);
      this.shuffle(videoIdArr);

      return videoIdArr;
    },
    updateRecommendedVideoIds() {
      // Vind index van video
      let videoIndex = this.videos.order.indexOf(this.playerVideo.id);

      // Maak een lijst van video IDs om aan te bevelen
      this.recommendedVideoIds = this.mergeArrays([
        this.findNearbyVideos(videoIndex, 2), // Suggereer een mix van video's die rond dezelfde datum zijn geüpload
        this.latestVideos.slice(0, 2).map(video => video.id), // Suggereer enkele nieuwste video's
        this.pickRandom(this.videos.order, 4) // Suggereer willekeurige video's
      ]).filter((video) => video != this.playerVideo.id);
    },
    setCurrentVideoId(videoId) {
      this.playerVideo = this.videos.values[videoId];
      this.updateRecommendedVideoIds();
    },
    testPageForVideo() {
      if (this.videos && this.$route.name == 'Video') {
        this.setCurrentVideoId(this.$route.params.videoId);
        this.isOnVideoPage = true;
      } else {
        this.isOnVideoPage = false;
      }
    },
    closePlayer() {
      this.playerVideo = null;
    },
    toggleBurgerMenu() {
      this.isBurgerMenuOpen = !this.isBurgerMenuOpen;
    },
    setCookie(name, value, days) { // https://stackoverflow.com/a/24103596
      var expires = "";
      if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + (value || "")  + expires + "; path=/; SameSite=None; Secure";
    },
    getCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
    },
    confirmCookies() {
      this.isCookieBannerOpen = false;
      this.setCookie('cookiesAccepted', true, 356);
      this.setAnalyticsScript();
    },
    setAnalyticsScript() {
      // Script 1
      let $script1 = document.createElement('script');
      $script1.type = "text/javascript"
      $script1.async = "true";
      $script1.src = "https://www.googletagmanager.com/gtag/js?id=G-6DTR3G4TS8";
      // Script 2
      let $script2 = document.createElement('script');
      $script2.type = "text/javascript"
      $script2.async = "true";
      $script2.innerHTML = "window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-6DTR3G4TS8');"
      // Bind aan pagina
      let $scriptOnPage = document.getElementsByTagName('script')[0];
      $scriptOnPage.parentNode.insertBefore($script1, $scriptOnPage);
      $scriptOnPage.parentNode.insertBefore($script2, $scriptOnPage);
    }
  },
  watch: {
    $route() {
      this.testPageForVideo();
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

    &:focus:focus-visible {
      outline: 2px solid $accentColor;
    }
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
  h2 {
    font-size: 2.5em;
    color: $headingColorBright;
  }
  svg.h2Icon {
    display: inline-block;
    font-size: 2.5em;
    margin-right: 60px;
    color: $headingColorBright;
  }
  a {
    position: relative;
    text-decoration: none;
    color: $linkColor;
    cursor: pointer;

    &.link::before {
      content: '';
      display: inline-block;
      position: absolute;
      bottom: 0; left: 0;
      height: 1px;
      width: 0;
      background-color: $linkColor;
      transition: width .2s ease-in-out;
    }
    &.link:hover::before, &.link:active::before, &.link:focus::before { width: 100%; }
  }
  button.btn, a.btn {
    display: inline-block;
    padding: 10px 16px;
    background-color: #4a4e69;
    color: rgb(221, 221, 221);
    border: 2px solid transparent;
    border-radius: 2px;
    font-weight: bold;
    font-size: .8em;
    cursor: pointer;
    transition: background-color .2s ease-in-out,
                border-color .2s ease-in-out,
                color .4s ease-in-out;
    &:hover, &:active, &:focus {
      background-color: #434764;
      border-color: rgba(0, 0, 0, .1);
      color: rgb(216, 216, 216);
    }
  }
  button.icon {
    background-color: transparent;
    color: white;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
</style>
