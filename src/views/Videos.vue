<template>
  <div id="viewVideos" class="view">
    <ChannelInfo :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
    <VideoUploads :videos="videos" :schoolYears="schoolYears" :playerVideo="playerVideo" />
  </div>
</template>

<script>
import ChannelInfo from '../components/videos/ChannelInfo.vue'
import VideoUploads from '../components/videos/VideoUploads.vue'

export default {
  name: 'Videos',
  components: {
    ChannelInfo,
    VideoUploads
  },
  props: {
    channelName: String,
    channelSubsFormatted: String,
    videos: Object,
    schoolYears: Object,
    playerVideo: Object
  }
}
</script>