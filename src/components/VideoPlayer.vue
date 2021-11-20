<template>
    <div class="videoPlayer" v-if="video" :class="{videoPage: isOnVideoPage}">
        <div class="video" ref="video" @click="pausePlay">
            <YouTube ref="youtube" class="youtube" :vars="playerVars" :width="videoWidth" :height="videoHeight" :src="video.id" @ready="loadVideo" @state-change="stateChange" />
            <div class="overlay">
                <button class="close" @click.stop="close"><fa icon="times" /></button>
                <button class="expand" @click.stop="expand"><fa icon="external-link-alt" rotation="270" /></button>
                <button class="playpause"></button>
                <div class="time" v-if="$refs.youtube">
                    <span class="currentTime" v-text="videoTime"></span>
                    <span class="divider"> / </span>
                    <span class="maxTime">{{video.duration}}</span>
                </div>
            </div>
        </div>
        <div class="timeline">

        </div>
        <div class="title">
            <h2>{{video.title}}</h2>
        </div>
    </div>
</template>

<script>
import YouTube from 'vue3-youtube'

export default {
    name: 'VideoPlayer',
    components: { YouTube },
    props: {
        video: Object,
        isOnVideoPage: Boolean
    },
    data() {
        return {
            videoWidth: 100,
            videoHeight: 100,
            videoTime: null,
            videoUpdateTimeInterval: null,
            prevPlayerState: 0
        }
    },
    computed: {
        playerVars() {
            return {
                modestbranding: 1,
                controls: 0,
                autoplay: 1
            }
        } 
    },
    methods: {
        loadVideo() {
            console.log('hi')
            this.$refs.youtube.playVideo()
            if (!this.isOnVideoPage) {
                this.setDimensionsMiniPlayer();
            }
        },
        setDimensionsMiniPlayer() {
            console.log('set!')
            let $video = this.$refs.video.firstChild;
            let width = 400;
            let height = width / 16 * 9 + 130;
            this.videoWidth = width;
            this.videoHeight = height;
            $video.firstChild.style.width = width + 'px';
            $video.firstChild.style.height = height + 'px';
        },
        pausePlay() {
            let $youtube = this.$refs.youtube;
            switch ($youtube.getPlayerState()) {
                case -1: // Als nog niet gestart
                case 2: // Als gepauzeerd
                    $youtube.playVideo();
                    break;

                case 1: // Als aan het afspelen
                    $youtube.pauseVideo();
                    break;

                default:
                    break;
            }
        },
        stateChange() {
            if (!this.$refs.youtube) return;
            let playerState = this.$refs.youtube.getPlayerState();
            console.log(this.prevPlayerState)
            console.log(playerState)
            if (playerState != this.prevPlayerState && playerState == 1) { // If playing
                this.videoUpdateTimeInterval = setInterval(this.updateVideoTime, 100);
            } else {
                clearInterval(this.videoUpdateTimeInterval);
            }
            this.prevPlayerState = playerState;
        },
        updateVideoTime() {
            this.videoTime = Math.floor(this.$refs.youtube.getCurrentTime());
            console.log('up');
        },
        expand() {
            this.$router.push({
                name: 'Video',
                path: '/videos/:videoId/:videoName',
                params: {
                    videoId: this.video.id,
                    videoName: this.video.videoPath
                }
            });
        },
        close() {
            let playerState = this.$refs.youtube.getPlayerState();
            if (playerState == this.prevPlayerState || playerState == 1) clearInterval(this.videoUpdateTimeInterval)
            this.$emit('close');
        }
    },
    watch: {
        isOnVideoPage() {
            this.setDimensionsMiniPlayer();
        }
    }
}
</script>

<style lang="scss" scoped>
    .videoPlayer {
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 400px;
        z-index: 10;

        &.videoPage {
            position: absolute;
            width: 100%;
            top: 200px;
            height: 100%;
            pointer-events: none;

            .video {
                left: calc(100vw * .2) !important;
                width: calc(100% * .6 * 4 / 5 - 20px) !important;
                height: calc(100vw * .6 * 4 / 5 / 16 * 9 - 10px) !important;
                pointer-events: auto;
                border-radius: 4px;

                .youtube > :first-child {
                    width: calc(100vw * .6 * 4 / 5) !important;
                    height: calc(100vw * .6 * 4 / 5 / 16 * 9 + 130px) !important;
                }
                .overlay {
                    display: none;
                }
            }
            .title {
                display: none;
            }
        }
    }
    .video {
        position: relative;
        overflow: hidden;

        &::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, .4);
            opacity: 0;
            transition: opacity .1s ease-in-out;
        }

        .youtube {
            pointer-events: none;
            margin-top: -130px;
            transform: translateY(62.5px);
        }
        .overlay {
            position: absolute;
            opacity: 0;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            z-index: 3;
        }
        button {
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: transparent;
            color: white;
            font-size: 20px;
            border: none;
            cursor: pointer;
            z-index: 1;

            &.expand {
                left: 20px;
                right: unset;
            }
        }

        &:hover {
            &::after { opacity: 1; }
            .overlay { opacity: 1; }
        }
    }
    .time {
        position: absolute;
        bottom: 10px;
        left: 20px;

        .currentTime {
            color: white;
        }
        .divider, .maxTime {
            color: rgb(204, 204, 204);
        }
    }
    .title {
        background-color: gray;
        height: 40px;
    }
</style>