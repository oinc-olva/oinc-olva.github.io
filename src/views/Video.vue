<template>
    <div class="video view" ref="video">
        <transition name="fade">
            <ShareLightBox v-if="isShareLightBoxOpen" :videoId="videoId" @close="isShareLightBoxOpen = false" />
        </transition>
        <div v-if="playerVideo" class="container">
            <div class="main">
                <div class="playerBg" />
                <div class="videoInfo">
                    <div class="mainInfo">
                        <h2 class="title">
                            {{playerVideo.title}}
                            <button class="share icon" @click="isShareLightBoxOpen = true"><fa icon="share-alt" /></button>
                        </h2>                        
                    </div>
                    <p class="generalInfo">{{playerVideo.views}} weergaven • {{playerVideo.publishDate}}</p>
                    <div class="description" v-if="playerVideo.description">{{playerVideo.description}}</div>
                </div>
            </div>
            <div class="sidebar" v-if="recommendedVideos">
                <h3>Enkele suggesties:</h3>
                <div class="videoContent">
                    <VideoPreview class="recommendedVideo" :key="video" v-for="video in recommendedVideos.slice(0, shownRecommendedVideos)" :video="video" />
                </div>
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
    .title {
        display: inline-block;
        color: white;
        font-weight: normal;
    }
    .share {
        margin: 0 20px;
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
        .videoContent {
            display: grid;
            border: 1px solid rgb(53, 53, 80);
            background-color: rgba(0, 0, 0, .1);
            border-radius: 4px;
            padding: 15px;
        }
        .showMore {
            display: block;
            margin: 30px auto;
        }
    }

    
    @media screen and (max-width: 1450px) {
        .mainInfo {
            flex-direction: column;
            align-items: unset;
        }
    }
    @media screen and (max-width: $videoPageRescale1Viewport) {
        .container {
            flex-direction: column;
            width: $videoPageRescale1WidthVw;
        }
        .main {
            margin-right: 0;
        }
        .sidebar {
            width: calc(100% - 40px);
            margin: 50px 20px;

            .videoContent {
                grid-template-columns: repeat( auto-fill, minmax(calc(120px + 5vw), 1fr) );
            }
        }
    }
    @media screen and (max-width: $videoPageRescale2Viewport) {
        .video {
            padding-top: 140px;
        }
        .container {
            width: $videoPageRescale2WidthVw;
        }
    }
</style>