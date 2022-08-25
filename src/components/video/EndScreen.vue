<template>
    <div id="endScreen">
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
    $apCloseButtonSize: 1.2em;

    #endScreen {
        display: flex;
        background: $videoBackground;
        overflow: hidden;
        color: $headingColor;
    }
    #autoPlayScreen {
        position: relative;
        flex: 1;
        background: $videoBackgroundBrighter;
        padding: $screenPadding;


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
        .videoPreview {
            width: 100%;
            padding: 10%;
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
    #recommendedScreen {
        display: flex;
        flex-direction: column;
        flex: 2;
        background: $videoBackground;
        padding: $screenPadding;

        #rsList {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(calc(200px + 7%), 1fr));
            padding: 0 calc(5px + 3%);
            list-style: none;
            height: 0;
            flex: 1;
            margin: 40px 0;
            overflow-y: scroll;

            li a {
                width: 100%;
                padding: 20px 40px;
                outline-offset: -10px;
            }
        }
    }
</style>