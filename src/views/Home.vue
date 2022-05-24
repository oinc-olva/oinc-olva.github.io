<template>
  <div id="viewHome" class="view">
    <HomeMoreVideos />
    <InstagramFeed />
  </div>
</template>

<script>
import HomeMoreVideos from '../components/home/HomeMoreVideos.vue'
import InstagramFeed from '../components/home/instagram/InstagramFeed.vue'

export default {
    name: 'Home',
    components: {
      HomeMoreVideos,
      InstagramFeed
    }
}
</script>