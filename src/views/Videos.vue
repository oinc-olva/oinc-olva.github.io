<template>
  <div id="viewVideos" class="view">
    <ChannelInfo :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
    <VideoUploads :uploads="channelUploads" :publishSchoolYears="publishSchoolYears" :playerVideo="playerVideo" />
  </div>
</template>

<script>
import ChannelInfo from '../components/ChannelInfo.vue'
import VideoUploads from '../components/VideoUploads.vue'

export default {
  name: 'Videos',
  components: {
    ChannelInfo,
    VideoUploads
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