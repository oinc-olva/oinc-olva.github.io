<template>
    <div id="viewVideo" class="view" ref="video">
        <transition name="fade">
            <ShareLightBox v-if="isShareLightBoxOpen" :url="getShareURL()" @close="isShareLightBoxOpen = false" />
        </transition>
        <div class="container" v-if="playerVideo">
            <section id="video">
                <div id="playerBackground" />
                <div id="videoMeta">
                    <div id="videoHeading">
                        <h2 id="videoTitle">
                            {{playerVideo.title}}
                            <button id="shareBtn" class="icon" @click="isShareLightBoxOpen = true" aria-label="Delen" title="Delen"><fa icon="share-alt" /></button>
                        </h2>                        
                    </div>
                    <p id="videoGeneralMeta">
                        <span id="videoMetaViews">{{playerVideo.views}} weergaven</span>
                        <span id="videoMetaDate">{{playerVideo.publishDate}}</span>
                    </p>
                    <div id="videoDesc" v-if="playerVideo.description">{{playerVideo.description}}</div>
                </div>
            </section>
            <aside id="sidebar" v-if="recommendedVideoIds">
                <div id="playlistContainer"><!-- Afspeellijst wordt aan dit element gekoppeld --></div>
                <VideoGallery title="Enkele suggesties" :videos="videos" :videoIds="recommendedVideoIds" :playerVideo="playerVideo" :shownVideoCount="shownRecommendedVideos" @increaseShownVideoCount="shownRecommendedVideos += 3" :isLoadedByRequest="false" />
            </aside>
        </div>
    </div>
</template>

<script>
import VideoGallery from '../components/videos/VideoGallery.vue'
import ShareLightBox from '../components/ShareLightBox.vue'

export default {
    name: 'Video',
    props: {
        recommendedVideoIds: Array,
        videos: Object,
        playerVideo: Object
    },
    components: {
        VideoGallery,
        ShareLightBox
    },
    data() {
        return {
            videoId: this.$route.params.videoId,
            shownRecommendedVideos: 4,
            isShareLightBoxOpen: false
        }
    },
    methods: {
        getShareURL() {
            return `${window.location.protocol}//${window.location.host}/v/${this.$route.params.videoId}`;
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
    #viewVideo {
        box-sizing: border-box;
        background-color: #21242e;
        padding-top: 200px;
        min-height: 100vh;

        .container {
            display: flex;
        }
    }
    #video {
        flex: 1;
        margin-right: 40px;
    }
    #playerBackground {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        background-color: #1a1d25;
        border-radius: 4px;
        margin-bottom: 25px;
        overflow: hidden;
    }
    #videoMeta {
        margin: 10px;
    }
    #videoTitle {
        display: inline-block;
        color: white;
        font-size: 1.8em;
        font-weight: normal;
    }
    #shareBtn {
        margin: 0 20px;
    }
    #videoGeneralMeta {
        color: $textColorGray;
        font-size: .9em;
        margin: 5px 0;
    }
    #videoMetaViews::after {
        content: '';
        display: inline-block;
        margin: .2em 5px;
        width: .2em;
        height: .2em;
        background-color: $textColorGray;
        border-radius: 50%;
    }
    #videoDesc {
        position: relative;
        color: $textColorGray;
        margin: 20px 0 40px 10px;
        border-left: 1px solid $textColorGray;
        white-space: pre-wrap;
        padding: 5px 0 5px 30px;
    }
    #sidebar {
        width: #{$videoPageSidebarWidthFrac * 100vw};
        margin-bottom: 50px;

        h2 {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: $headingColor;
        }
    }
    #showMoreBtn {
        display: block;
        margin: 30px auto;
    }
    
    @media screen and (max-width: 1450px) {
        #videoHeading {
            flex-direction: column;
            align-items: unset;
        }
    }
    @media screen and (max-width: $videoPageRescale1Viewport) {
        .container {
            flex-direction: column;
            width: $videoPageRescale1WidthVw;
        }
        #video {
            margin-right: 0;
        }
        #sidebar {
            width: calc(100% - 40px);
            margin: 50px 20px;
        }
    }
    @media screen and (max-width: $videoPageRescale2Viewport) {
        #viewVideo {
            padding-top: 140px;
        }
        .container {
            width: $videoPageRescale2WidthVw;
        }
    }
</style>