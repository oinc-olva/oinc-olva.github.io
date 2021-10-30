<template>
  <div class="videos">
    <ChannelInfo :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
    <VideoGallery :uploads="channelUploads" :publishSchoolYears="publishSchoolYears" />
  </div>
</template>

<script>
import ChannelInfo from '../components/ChannelInfo.vue'
import VideoGallery from '../components/VideoGallery.vue'

export default {
  name: 'Videos',
  components: {
    ChannelInfo,
    VideoGallery
  },
  props: {
    channelName: String,
    channelSubsFormatted: String,
    channelUploads: Object,
    publishSchoolYears: Array
  }
}
</script>