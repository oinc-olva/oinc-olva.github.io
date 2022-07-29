<template>
  <div id="viewVideos" class="view">
    <ChannelInfo :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
    <PlaylistGallery :playlists="playlists" :videos="videos" />
    <VideoUploads :videos="videos" :schoolYears="schoolYears" :playerVideo="playerVideo" />
  </div>
</template>

<script>
import ChannelInfo from '../components/videos/ChannelInfo.vue'
import PlaylistGallery from '../components/videos/PlaylistGallery.vue'
import VideoUploads from '../components/videos/VideoUploads.vue'

export default {
  name: 'Videos',
  components: {
    ChannelInfo,
    PlaylistGallery,
    VideoUploads
  },
  props: {
    channelName: String,
    channelSubsFormatted: String,
    videos: Object,
    playlists: Array,
    schoolYears: Object,
    playerVideo: Object
  }
}
</script>