<template>
  <div id="viewVideos" class="view">
    <ChannelInfo :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
    <VideoGallery :uploads="channelUploads" :publishSchoolYears="publishSchoolYears" :playerVideo="playerVideo" />
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
    publishSchoolYears: Array,
    playerVideo: Object
  }
}
</script>