<template>
    <div class="dragOverlay" v-if="isDragging" @mousemove="dragTimeline" @mouseup="endHoveringTimeline" />
    <div class="videoPlayer" v-if="video" :class="{videoPage: isOnVideoPage}">
        <div :class="['playerContainer', {draggingTimeline: this.isDragging}]">
            <div class="video" ref="video" @click="pausePlay">
                <YouTube ref="youtube" class="youtube" :vars="playerVars" :width="videoWidth" :height="videoHeight" :src="video.id" @ready="loadVideo" @state-change="stateChange" />
                <div class="overlay">
                    <button class="close" @click.stop="close"><fa icon="times" /></button>
                    <button class="expand" @click.stop="expand"><fa icon="external-link-alt" rotation="270" /></button>
                    <button class="playpause"></button>
                    <div class="time" v-if="$refs.youtube">
                        <span class="currentTime">{{videoTimeSecFormatted}}</span>
                        <span class="divider"> / </span>
                        <span class="maxTime">{{video.durationFormatted}}</span>
                    </div>
                </div>
            </div>
            <div :class="['timeline', {dragging: this.isDragging}]" @mousemove="calculateHoveredTimelineTime" @mousedown="startDragTimeline">
                <div class="background"></div>
                <div class="timeLoaded" :style="{width: this.videoLoadedFrac * 100 + '%'}"></div>
                <div class="currentTime" :style="{width: this.videoTimeSec / this.video.durationSec * 100 + '%'}"></div>
                <div class="hoverTimeTooltip" :style="{left: this.relativeMouseX + 'px'}">{{this.videoTimeHoveringFormatted}}</div>
            </div>
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
    emits: [ 'close' ],
    data() {
        return {
            videoWidth: 100,
            videoHeight: 100,
            videoTimeSec: 0,
            videoTimeSecFormatted: '0:00',
            videoTimeHovering: 0,
            videoTimeHoveringFormatted: '0:00',
            relativeMouseX: 0,
            videoLoadedFrac: 0,
            videoUpdateTimeInterval: null,
            prevPlayerState: 0,
            playerStateBeforeDrag: null,
            isDragging: false
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
            this.$refs.youtube.playVideo()
            if (!this.isOnVideoPage) this.setDimensionsMiniPlayer();
        },
        setDimensionsMiniPlayer() {
            let $video = this.$refs.video.firstChild;
            let width = 400;
            let height = width / 16 * 9 + 130;
            this.videoWidth = width;
            this.videoHeight = height;
            $video.firstChild.style.width = width + 'px';
            $video.firstChild.style.height = height + 'px';
        },
        formatTimeSec(sec) {
            let formattedTime = [];
            let secLeft = sec;
            for (let i = 0; i < this.video.durationFormattedParts; i++) {
                let weight = Math.pow(60, this.video.durationFormattedParts - 1 - i);
                let amount = Math.floor(secLeft / weight);
                secLeft -= amount * weight;
                if (i != 0 && amount < 10) amount = '0' + amount;
                formattedTime.push(amount);
            }
            return formattedTime.join(':')
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
            if (playerState != this.prevPlayerState && playerState == 1) { // If playing
                this.videoUpdateTimeInterval = setInterval(this.updateVideoTime, 100);
            } else {
                clearInterval(this.videoUpdateTimeInterval);
            }
            this.prevPlayerState = playerState;
        },
        updateVideoTime() {
            this.setVideoTime(this.$refs.youtube.getCurrentTime());
        },
        setVideoTime(timeSec) {
            this.videoTimeSec = Math.floor(timeSec);
            this.videoLoadedFrac = this.$refs.youtube.getVideoLoadedFraction();
            this.videoTimeSecFormatted = this.formatTimeSec(this.videoTimeSec);

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
        },
        calculateHoveredTimelineTime(e) {
            console.log('hovering')
            this.relativeMouseX = e.clientX - this.$refs.video.getBoundingClientRect().left;
            let videoWidth = this.$refs.video.clientWidth;
            if (this.relativeMouseX < 0) {
                this.relativeMouseX = 0;
            } else if (this.relativeMouseX > videoWidth) {
                this.relativeMouseX = videoWidth;
            }
            this.videoTimeHovering = Math.floor(this.relativeMouseX / videoWidth * this.video.durationSec);
            this.videoTimeHoveringFormatted = this.formatTimeSec(this.videoTimeHovering);
        },
        endHoveringTimeline() {
            if (this.playerStateBeforeDrag == 1 || this.playerStateBeforeDrag == 3) this.$refs.youtube.playVideo();
            this.playerStateBeforeDrag = null;
            this.isDragging = false;
        },
        startDragTimeline() {
            this.playerStateBeforeDrag = this.$refs.youtube.getPlayerState();
            this.isDragging = true;
            this.$refs.youtube.pauseVideo();
            this.seekToHoveredTime();
        },
        dragTimeline(e) {
            this.calculateHoveredTimelineTime(e)
            this.seekToHoveredTime();
        },
        seekToHoveredTime() {
            this.setVideoTime(this.videoTimeHovering);
            this.$refs.youtube.seekTo(this.videoTimeHovering);
            this.stateChange();
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
    .dragOverlay {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        cursor: pointer;
        z-index: 20;
    }
    .videoPlayer {
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 400px;
        box-shadow: 0 0 20px 4px rgba(0, 0, 0, .3);
        z-index: 10;

        &.videoPage {
            position: absolute;
            width: 100%;
            top: 200px;
            height: 100%;
            box-shadow: none;
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
    .playerContainer {
        &:hover, &.draggingTimeline {
            .video::after { opacity: 1; }
            .overlay { opacity: 1; }
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
            transform: translateY(65px);
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
    }
    .time {
        position: absolute;
        bottom: 10px;
        left: 20px;
        pointer-events: none;
        user-select: none;

        .currentTime {
            color: white;
        }
        .divider, .maxTime {
            color: rgb(204, 204, 204);
        }
    }
    .timeline {
        position: absolute;
        width: 100%;
        height: 2px;
        padding: 6px 0;
        transform: translateY(-50%);
        cursor: pointer;
        z-index: 8;

        &:hover, &.dragging {
            .background, .timeLoaded, .currentTime {
                height: 5px;
                transform: translateY(-3px);
            }
            .currentTime::after { transform: scale(1); }
            .hoverTimeTooltip { opacity: 1; }
        }

        .background, .timeLoaded, .currentTime {
            position: absolute;
            left: 0;
            top: 50%;
            height: 2px;
            background-color: rgba(200, 200, 200, .3);
            transition: 
                height .1s ease-in-out,
                transform .1s ease-in-out;
        }
        .background {
            width: 100%;
        }
        .currentTime {
            position: relative;
            background-color: rgb(85, 199, 228);

            &::after {
                content: '';
                display: inline-block;
                position: absolute;
                top: -2.5px;
                right: -5px;
                width: 10px;
                height: 10px;
                background-color: rgb(85, 199, 228);
                border-radius: 50%;
                transform: scale(0);
                transition: transform .1s ease-in-out;
            }
        }
        .hoverTimeTooltip {
            position: absolute;
            transform: translateX(-50%);
            top: -40px;
            background-color: #21242e;
            padding: 5px 10px;
            border-radius: 3px;
            color: white;
            opacity: 0;
            pointer-events: none;
            transition: opacity .3s ease-in-out;
        }
    }
    .title {
        position: relative;
        box-sizing: border-box;
        background-color: #393f50;
        height: 40px;
        z-index: -1;

        h2 {
            position: absolute;
            top: calc(50% + 1px);
            font-size: .8em;
            padding-left: 10px;
            color: #a2a9da;
            transform: translateY(-50%);
        }
    }
</style>