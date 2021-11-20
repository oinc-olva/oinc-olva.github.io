<template>
    <div class="video" ref="video">
        <div v-if="playerVideo" class="container">
            <div class="main">
                <div class="playerBg">
                </div>
                <div class="videoInfo">
                    <h2 class="title">{{playerVideo.title}}</h2>
                    <p class="generalInfo">{{playerVideo.views}} weergaven • {{playerVideo.publishDate}}</p>
                    <div class="share"></div>
                    <div class="description" v-if="playerVideo.description">{{playerVideo.description}}</div>
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
        latestVideos: Array,
        playerVideo: Object
    },
    components: {
        VideoPreview
    },
    data() {
        return {
            videoId: this.$route.params.videoId
        }
    },
    beforeRouteUpdate(to, _, next) {
        this.videoId = to.params.videoId
        next()
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
    .main {
        flex: 4;
        margin-right: 40px;
    }
    .playerBg {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        background-color: rgba(0, 0, 0, .2);
        border-radius: 4px;
        margin-bottom: 20px;
        overflow: hidden;
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