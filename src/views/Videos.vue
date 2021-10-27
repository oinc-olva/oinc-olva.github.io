<template>
  <div class="videos">
    <ChannelInfo :channelName="channelName" :channelSubsFormatted="channelSubsFormatted" />
  </div>
</template>

<script>
import ChannelInfo from '../components/ChannelInfo.vue'

export default {
  name: 'Videos',
  components: {
    ChannelInfo
  },
  props: {
    channelName: String,
    channelSubsFormatted: String
  }
}
</script>