<template>
    <div class="video" ref="video">
        <transition name="fade">
            <ShareLightBox v-if="isShareLightBoxOpen" :videoId="videoId" @close="isShareLightBoxOpen = false" />
        </transition>
        <div v-if="playerVideo" class="container">
            <div class="main">
                <div class="playerBg" />
                <div class="videoInfo">
                    <div class="mainInfo">
                        <h2 class="title">{{playerVideo.title}}</h2>
                        <div class="links" v-if="playerVideo">
                            <button class="share icon" @click="isShareLightBoxOpen = true"><fa icon="share-alt" /></button>
                            <a :href="`https://www.youtube.com/watch?v=${playerVideo.id}`" target="_blank"><button class="disclaimer">Videospeler ontwikkeld met <img class="youtubeLogo" src="../assets/youtube_logo.png" alt="YouTube"></button></a>
                        </div>
                    </div>
                    <p class="generalInfo">{{playerVideo.views}} weergaven • {{playerVideo.publishDate}}</p>
                    <div class="description" v-if="playerVideo.description">{{playerVideo.description}}</div>
                </div>
            </div>
            <div class="sidebar" v-if="recommendedVideos">
                <h3>Enkele suggesties:</h3>
                <VideoPreview class="recommendedVideo" :key="video" v-for="video in recommendedVideos.slice(0, shownRecommendedVideos)" :video="video" />
                <button class="showMore btn" @click="shownRecommendedVideos += 3" v-if="recommendedVideos.length > shownRecommendedVideos">Meer tonen</button>
            </div>
        </div>
    </div>
</template>

<script>
import VideoPreview from '../components/VideoPreview.vue'
import ShareLightBox from '../components/ShareLightBox.vue'

export default {
    name: 'Video',
    props: {
        recommendedVideos: Array,
        playerVideo: Object
    },
    components: {
        VideoPreview,
        ShareLightBox
    },
    data() {
        return {
            videoId: this.$route.params.videoId,
            shownRecommendedVideos: 4,
            isShareLightBoxOpen: false
        }
    },
    beforeRouteUpdate(to, _, next) {
        this.videoId = to.params.videoId;
        this.shownRecommendedVideos = 4;
        next();
    }
}
</script>

<style lang="scss" scoped>
    .fade-enter-active { transition: opacity .2s ease-in-out; }
    .fade-enter-from { opacity: 0; }
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
        flex: 1;
        margin-right: 40px;
    }
    .playerBg {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        background-color: rgba(0, 0, 0, .2);
        border-radius: 4px;
        margin-bottom: 25px;
        overflow: hidden;
    }
    .videoInfo {
        margin: 10px;
    }
    .mainInfo, .mainInfo .links, .disclaimer {
        display: flex;
        align-items: center;
    }
    .title {
        color: white;
        font-weight: normal;
        flex: 1;
    }
    .share {
        margin: 0 30px;
    }
    .disclaimer {
        position: relative;
        padding: 5px;
        padding-left: 15px;
        background-color: #282828 !important;
        border: 1px solid rgb(99, 99, 99);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        transition: border-color .3s ease-in-out;
        &:hover {
            border-color: $accentColor;
            &::after { opacity: 1; }
        }

        &::after {
            content: '► Deze video bekijken op';
            display: block;
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            opacity: 0;
            padding: .7em 15px;
            border-radius: 10px;
            text-align: left;
            background-color: #282828;
            transition: opacity .2s ease-in-out;
        }

        img {
            height: 30px;
            z-index: 2;
        }
    }
    .generalInfo {
        color: gray;
        font-size: .9em;
        margin: 5px 0;
    }
    .description {
        position: relative;
        color: rgb(143, 143, 143);
        margin: 20px 0 100px 10px;
        border-left: 1px solid rgb(73, 73, 73);
        white-space: pre-wrap;
        padding: 5px 0 5px 30px;
    }
    .sidebar {
        width: $videoPageSidebarWidth;
        margin-bottom: 50px;

        h3 {
            color: rgb(106, 105, 170);
            margin-bottom: 10px;
        }
        .showMore {
            display: block;
            margin: 30px auto;
        }
    }
    .videoPreview {
        width: 100%;
    }
</style>