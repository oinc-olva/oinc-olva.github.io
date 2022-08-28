<template>
    <div id="endScreen" :class="{onVideoPage: isOnVideoPage}">
        <div id="autoPlayScreen" v-if="isAutoplay && !isAutoplayCancelled">
            <button id="apCloseButton" class="icon" @click="cancelAutoplay" title="Autoplay annuleren" aria-label="Autoplay annuleren" tabindex="4"><fa icon="times" /></button>
            <div id="apTimerBar">
                <div id="apTimerProgress"></div>
            </div>
            <div id="apMainContent">
                <h3 id="apTimerSub">Over {{autoplayCountdown}} seconden...</h3>
                <VideoPreview :video="videos.values[recommendedVideoIds[0]]" :isPlaying="false" tabindex="4" />
                <div id="apOptions">
                    <button id="apCancel" class="btn" @click="cancelAutoplay" aria-label="Autoplay annuleren" tabindex="4">Annuleren</button>
                    <button id="apContinue" class="btn" @click="continueAutoplay" aria-label="Autoplay verderzetten" tabindex="4">Afspelen</button>
                </div>
            </div>
        </div>
        <div id="recommendedScreen">
            <h3 id="rsTitle">Misschien kijkt u ook naar...</h3>
            <ul id="rsList" aria-label="Suggesties" tabindex="4">
                <li v-for="videoId of ( !isAutoplay || isAutoplayCancelled ? recommendedVideoIds: recommendedVideoIds.slice(1) )" :key="videoId">
                    <VideoPreview :video="videos.values[videoId]" :isPlaying="false" tabindex="4" />
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import VideoPreview from '../videos/VideoPreview.vue'

export default {
    name: 'EndScreen',
    components: {
        VideoPreview
    },
    props: {
        videos: Object,
        recommendedVideoIds: Array,
        isOnVideoPage: Boolean,
        isAutoplay: Boolean
    },
    emits: [ 'setCurrentVideoId' ],
    data() {
        return {
            isAutoplayCancelled: false,
            autoplayInterval: null,
            autoplayCountdown: 10
        }
    },
    methods: {
        startAutoplay() {
            this.autoplayInterval = setInterval(() => {
                this.autoplayCountdown--;
                if (this.autoplayCountdown == 0) {
                    clearInterval(this.autoplayInterval);
                    this.continueAutoplay();
                }
            }, 1000);
        },
        cancelAutoplay() {
            this.isAutoplayCancelled = true;
            clearInterval(this.autoplayInterval);
        },
        continueAutoplay() {
            if (this.$route.name == 'Video') {
                this.$router.push({
                    name: 'Video',
                    path: '/videos/:videoId/:videoPath',
                    params: {
                        videoId: this.recommendedVideoIds[0],
                        videoPath: this.videos.values[this.recommendedVideoIds[0]].videoPath
                    }
                });
            } else {
                this.$emit('setCurrentVideoId', this.recommendedVideoIds[0]);
            }
        },
        escapePressed(e) {
            if (e.key == 'Escape' && !this.isAutoplayCancelled) this.cancelAutoplay();
        }
    },
    mounted() {
        if (this.isAutoplay) this.startAutoplay();
        document.addEventListener('keyup', this.escapePressed, false);
    },
    unmounted() {
        clearInterval(this.autoplayInterval)
        document.removeEventListener('keyup', this.escapePressed, false);
    },
    watch: {
        isAutoplay(bool) {
            if (!bool) {
                clearInterval(this.autoplayInterval);
            } else {
                if (!this.isAutoplayCancelled) {
                    this.autoplayCountdown = 10;
                    this.startAutoplay();
                }
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    $screenPadding: 40px;
    $screenPaddingSlimmer: 20px;
    $screenPaddingSlimmest: 15px;
    $apCloseButtonSize: 1.2em;

    #endScreen {
        display: flex;
        background: $videoBackground;
        overflow: hidden;
        color: $headingColor;

        &:not(.onVideoPage) {
            #apMainContent {
                height: calc(100% - 60px) !important;
            }
            #autoPlayScreen + #recommendedScreen {
                display: none;
            }
            #autoPlayScreen {
                padding: $screenPaddingSlimmer $screenPaddingSlimmest;
    
                #apCloseButton {
                    display: none;
                }
                #apTimerBar {
                    visibility: hidden;
                    width: 100%;
                    height: 0 !important;
                    margin: 0 !important;
                }
                #apTimerSub {
                    text-align: center;
                }
                .videoPreview {
                    height: 80%;
                    padding: 6% 10%;
                    flex-direction: row;
                    text-align: left;
                }
                #apOptions button {
                    padding: 5px 16px;
                }
            }
            #recommendedScreen {
                padding: $screenPaddingSlimmer;

                #rsTitle {
                    display: none;
                }
                #rsList {
                    display: block !important;
                    margin: 25px 10px !important;

                    li {
                        width: 100%;
                        margin: 0;

                        .videoPreview {
                            height: 80%;
                            text-align: left;
                            flex-direction: row;
                        }
                    }
                }
            }
        }
    }
    #autoPlayScreen {
        position: relative;
        flex: 1;
        background: $videoBackgroundBrighter;
        padding: $screenPadding;
        width: 100%;
        box-sizing: border-box;

        h3 { font-size: 1em; }
        #apCloseButton {
            position: absolute;
            top: $screenPadding;
            right: $screenPadding;
            font-size: $apCloseButtonSize;
        }
        #apTimerBar {
            width: calc(100% - #{$apCloseButtonSize + .7em});
            height: 4px;
            background: rgba(255, 255, 255, .1);
            margin-top: #{$apCloseButtonSize * .5};
            margin-bottom: 15px;

            #apTimerProgress {
                height: 100%;
                background-color: $accentColor;
                animation: countDown 10s linear;
                @keyframes countDown {
                    from { width: 0; }
                    to { width: 100%; }
                }
            }
        }
        #apMainContent {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: calc(100% - #{60px + $screenPadding * .5});
        }
        #apOptions {
            display: flex;
            width: 100%;

            button {
                margin: 0 20px;
                flex: 1;
            }
            #apCancel {
                background: #333749;
            }
        }
    }
    .videoPreview {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        padding: 10%;
    }
    #recommendedScreen {
        display: flex;
        flex-direction: column;
        flex: 2;
        background: $videoBackground;
        padding: $screenPadding;

        #rsList {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(calc(200px + 3%), 1fr));
            padding: 0 calc(5px + 3%);
            list-style: none;
            height: 0;
            flex: 1;
            margin: 40px 0;
            overflow-x: hidden;
            overflow-y: scroll;

            li a {
                width: 100%;
                padding: 20px 40px;
                outline-offset: -10px;
            }
        }
    }
    @media screen and (max-width: 920px) {
        #endScreen.onVideoPage {
            #autoPlayScreen + #recommendedScreen {
                display: none;
            }
            #autoPlayScreen {
                padding: $screenPadding calc(20%);
    
                #apTimerBar {
                    width: 100%;
                }
                .videoPreview {
                    height: 80%;
                    text-align: left;
                    flex-direction: row;
                }
            }
        }
    }
    @media screen and (max-width: 650px) {
        #endScreen.onVideoPage {
            #recommendedScreen {
                padding: $screenPaddingSlimmer;
            }
            #rsList {
                display: block !important;
                margin-top: 10px !important;

                li {
                    width: 80%;
                    margin: 0 10%;

                    .videoPreview {
                        height: 80%;
                        text-align: left;
                        flex-direction: row;
                    }
                }
            }
        }
    }
    @media screen and (max-width: 600px) {
        #endScreen.onVideoPage {
            #apMainContent {
                height: calc(100% - 60px) !important;
            }
            #apTimerSub {
                text-align: center;
            }
            #apTimerBar {
                visibility: hidden;
                height: 0 !important;
                margin: 0 !important;
            }
            #autoPlayScreen .videoPreview {
                padding: 6% 10%;
            }
            #apOptions button {
                padding: 5px 16px;
            }
        }
    }
    @media screen and (max-width: 480px) {
        #endScreen.onVideoPage {
            #autoPlayScreen {
                padding-top: $screenPaddingSlimmest;
                padding-left: $screenPaddingSlimmest;
                padding-right: $screenPaddingSlimmest;

                #apCloseButton {
                    top: $screenPaddingSlimmest !important;
                    right: $screenPaddingSlimmest !important;
                }
            }
            #recommendedScreen li {
                width: 100%;
                margin: 0;
            }
        }
    }
    @media screen and (max-width: 400px) {
        #endScreen.onVideoPage {
            #rsTitle {
                display: none;
            }
        }
    }
</style>