<template>
    <div id="viewVideo" class="view" ref="video">
        <transition name="fade">
            <ShareLightBox v-if="isShareLightBoxOpen" :videoId="videoId" @close="isShareLightBoxOpen = false" />
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
            <aside id="sidebar" v-if="recommendedVideos">
                <h2>Enkele suggesties:</h2>
                <ul id="sidebarRecommended">
                    <li :key="video" v-for="video in recommendedVideos.slice(0, shownRecommendedVideos)">
                        <VideoPreview class="recommendedVideo" :video="video" />
                    </li>
                </ul>
                <button id="showMoreBtn" class="btn" @click="shownRecommendedVideos += 3" v-if="recommendedVideos.length > shownRecommendedVideos">Meer tonen</button>
            </aside>
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
        margin: 20px 0 100px 10px;
        border-left: 1px solid $textColorGray;
        white-space: pre-wrap;
        padding: 5px 0 5px 30px;
    }
    #sidebar {
        width: $videoPageSidebarWidth;
        margin-bottom: 50px;

        h2 {
            font-size: 1.2em;
            margin-bottom: 10px;
            color: $headingColor;
        }
    }
    #sidebarRecommended {
        display: grid;
        border: 1px solid rgb(53, 53, 80);
        background-color: rgba(0, 0, 0, .1);
        border-radius: 4px;
        padding: 15px;

        li {
            list-style: none;

            a { width: 100%; }
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
        #sidebarRecommended {
            grid-template-columns: repeat( auto-fill, minmax(calc(120px + 5vw), 1fr) );
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