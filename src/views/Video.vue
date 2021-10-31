<template>
    <div class="video" ref="video">
        <div v-if="videoData" class="container">
            <div class="player">
                <div class="ytVideo">
                    <iframe ref="ytVideo" @load="resize" :src="`https://www.youtube-nocookie.com/embed/${this.videoId}?modestbranding=1&showinfo=0`" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                <div class="videoInfo">
                    <h2 class="title">{{videoData.title}}</h2>
                    <p class="generalInfo">{{videoData.views}} weergaven • {{videoData.publishDate}}</p>
                    <div class="share"></div>
                    <div class="description" v-if="videoData.description">{{videoData.description}}</div>
                </div>
            </div>
            <div class="sidebar">
                <h3>Laatste video's:</h3>
                <VideoPreview class="recommendedVideo" :key="video" v-for="video in latestVideos.slice(0, 4)" :video="video" />
            </div>
        </div>
    </div>
</template>

<script>
import VideoPreview from '../components/VideoPreview.vue'

export default {
    name: 'Video',
    props: {
        channelUploads: Object,
        latestVideos: Array
    },
    components: {
        VideoPreview
    },
    data() {
        return {
            videoId: this.$route.params.videoId,
            ro: new ResizeObserver(this.resize)
        }
    },
    computed: {
        videoData() {
            for (let videos of Object.values(this.channelUploads))
                for (let i = 0; i < videos.length; i++)
                    if (videos[i].id == this.videoId) return videos[i]
        }
    },
    methods: {
        resize() {
            let $ytVideo = this.$refs.ytVideo
            if (!$ytVideo) return false;
            let $parent = $ytVideo.parentElement;
            $ytVideo.setAttribute('width', $parent.offsetWidth)
            $ytVideo.setAttribute('height', $parent.offsetHeight)
        }
    },
    beforeRouteUpdate(to, _, next) {
        this.videoId = to.params.videoId
        next()
    },
    mounted() {
        this.ro.observe(this.$refs.video)
    },
    beforeUnmount() {
        this.ro.unobserve(this.$refs.video)
    }
}
</script>

<style lang="scss" scoped>
    .video {
        box-sizing: border-box;
        background-color: #21242e;
        padding-top: 200px;
        min-height: 100vh;

        .container {
            display: flex;
        }
    }
    .player {
        flex: 4;
        margin-right: 40px;
    }
    .ytVideo {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        background-color: rgba(0, 0, 0, .2);
        border-radius: 4px;
        margin-bottom: 20px;
        overflow: hidden;

        iframe {
            position: absolute;
            top: 0;
        }
    }
    .videoInfo {
        margin: 10px;
    }
    .title {
        color: white;
        font-weight: normal;
    }
    .generalInfo {
        color: gray;
        font-size: .9em;
        margin: 5px 0;
    }
    .description {
        position: relative;
        color: rgb(143, 143, 143);
        margin-top: 20px;
        margin-left: 10px;
        border-left: 1px solid rgb(73, 73, 73);
        padding: 5px 0 5px 30px;
    }
    .sidebar {
        flex: 1;

        h3 {
            color: rgb(106, 105, 170);
            margin-bottom: 10px;
        }
    }
    .videoPreview {
        width: 100%;
    }
</style>