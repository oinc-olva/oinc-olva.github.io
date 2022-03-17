<template>
  <div id="viewHome" class="view">
    <HomeMoreVideos />
    <InstagramFeed />
  </div>
</template>

<script>
import HomeMoreVideos from '../components/HomeMoreVideos.vue'
import InstagramFeed from '../components/InstagramFeed.vue'

export default {
    name: 'Home',
    components: {
      HomeMoreVideos,
      InstagramFeed
    }
}
</script>