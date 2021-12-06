<template>
    <div class="videoPlayerWrapper" ref="videoPlayerWrapper" :class="{videoPage: isOnVideoPage}">
        <div class="dragOverlay" v-if="draggingType != 0" @mousemove="drag" @mouseup="endDrag" />
        <div class="videoPlayer" v-if="video" @dragstart="preventDefault">
            <div :class="['playerContainer', {dragging: draggingType != 0, paused: isPaused, buffering: isBuffering, pbrModalOpen: isPlaybackRateModalOpen, idle: isIdle}]">
                <div class="video" ref="video" v-on="{ click: isOnVideoPage ? null : () => pausePlay(false)}">
                    <YouTube ref="youtube" class="youtube" :vars="playerVars" :width="videoWidth" :height="videoHeight" :src="video.id" @ready="loadVideo" @state-change="stateChange" draggable="false" />
                    <div class="clickToPause" v-if="isOnVideoPage" @click.stop="pausePlay(true)" @mousemove="resetIdleTimer" @mouseleave="clearIdleTimer" />
                    <div class="overlay">
                        <button class="close icon" @click.stop="close"><fa icon="times" /></button>
                        <button class="expand icon" @click.stop="expand"><fa icon="external-link-alt" rotation="270" /></button>
                        <div class="controls">
                            <button class="pausePlay icon" @click.stop="pausePlay(false)"><fa :icon="isPaused ? 'play' : 'pause'" /></button>
                            <button class="volume icon" @mouseover="this.isVolumeWrapperOpen = true"><fa :icon="this.isMuted ? 'volume-mute' : (this.volume == 0 ? 'volume-off' : (this.volume < 70 ? 'volume-down' : 'volume-up'))" /></button>
                            <div class="time" v-if="$refs.youtube">
                                <span class="currentTime">{{videoTimeSecFormatted}}</span>
                                <span class="divider"> / </span>
                                <span class="maxTime">{{video.durationFormatted}}</span>
                            </div>
                            <div class="floatRight" v-if="isOnVideoPage">
                                <button class="playbackRate icon" @click.stop="togglePlaybackRateModal"><fa icon="tachometer-alt" /></button>
                                <button class="miniplayer icon" @click="gotoVideos"><fa icon="external-link-alt" rotation="90" /></button>
                                <button class="fullscreen icon" @click="toggleFullscreenMode"><fa :icon="this.isInFullscreenMode ? 'compress' : 'expand'" /></button>
                            </div>
                        </div>
                    </div>
                    <div class="status">
                        <img class="pauseIcon statusIcon" src="../assets/pause.svg" alt="Video Paused">
                        <div class="loadingIcon statusIcon" />
                    </div>
                </div>
                <div class="volumeSliderOuterWrapper" ref="volumeSliderOuterWrapper" v-if="isVolumeWrapperOpen" @mouseleave="mouseLeaveVolumeSliderWrapper">
                    <div class="volumeSliderInnerWrapper" @mousedown="startDragVolumeSlider">
                        <div class="volumeSlider" ref="volumeSlider">
                            <div class="volumeSliderLevel" :style="{height: this.isMuted ? '0' : this.volume + '%'}" />
                        </div>
                    </div>
                    <button class="muteAudio icon" @click="toggleMute"></button>
                </div>
                <div class="playbackRateModal" v-if="isPlaybackRateModalOpen" ref="playbackRateModal">
                    <ul>
                        <li :key="option" v-for="option in availablePlaybackRates" :class="{selected: this.playbackRate == option}" @click="setPlaybackRate(option)">{{option}}</li>
                    </ul>
                </div>
                <div :class="['timeline', {dragging: this.draggingType == 1}]" ref="timeline" @mousemove="calculateHoveredTimelineTime" @mousedown="startDragTimeline">
                    <div class="background"></div>
                    <div class="timeLoaded" :style="{width: this.videoLoadedFrac * 100 + '%'}"></div>
                    <div class="currentTime" :style="{width: this.videoTimeSec / this.video.durationSec * 100 + '%'}"></div>
                    <div class="hoverTimeTooltip" :style="{left: this.relativeMouseX + 'px'}">{{this.videoTimeHoveringFormatted}}</div>
                </div>
            </div>
            <div class="title" @click="expand">
                <h2>{{video.title}}</h2>
            </div>
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
            volume: 100,
            isMuted: false,
            relativeMouseX: 0,
            videoLoadedFrac: 0,
            videoUpdateTimeInterval: null,
            isVolumeWrapperOpen: false,
            currentPlayerState: 0,
            isPaused: false,
            isBuffering: false,
            isIdle: false,
            idleTimer: null,
            playerStateBeforeDrag: null,
            isInFullscreenMode: false,
            availablePlaybackRates: null,
            playbackRate: 1,
            isPlaybackRateModalOpen: false,
            draggingType: 0 // 0 -> niets; 1 -> tijdlijn; 2 -> volume
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
        preventDefault(e) {
            e.preventDefault();  
        },
        loadVideo() {
            this.$refs.video.firstChild.firstChild.setAttribute('tabindex', -1);
            this.availablePlaybackRates = this.$refs.youtube.getAvailablePlaybackRates();
            this.volume = this.$refs.youtube.getVolume();
            this.isMuted = this.$refs.youtube.isMuted();
            this.isPaused = false;
            if (!this.isOnVideoPage) this.setDimensionsMiniPlayer();
        },
        setDimensionsMiniPlayer() {
            let $video = this.$refs.video.firstChild;
            let width = 400;
            let height = width / 16 * 9;
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
        isCursorInElement(e, $el) {
            let rect = $el.getBoundingClientRect();
            return e.clientY > rect.top && e.clientY < rect.bottom && e.clientX > rect.left && e.clientX < rect.right;
        },
        pausePlay(resetIdleTimer) {
            if (this.isPlaybackRateModalOpen) {
                this.isPlaybackRateModalOpen = false;
                this.resetIdleTimer();
                return;
            }
            let playerState = this.$refs.youtube.getPlayerState();
            if (playerState == -1 || playerState == 2) { // Als nog niet gestart of gepauzeerd
                this.$refs.youtube.playVideo();
                this.isPaused = false;
                if (resetIdleTimer) this.resetIdleTimer();
            } else if (playerState == 1) { // Als aan het afspelen
                this.$refs.youtube.pauseVideo();
                this.isPaused = true;
                this.clearIdleTimer();
            }
            console.log(resetIdleTimer)
        },
        toggleMute() {
            this.isMuted = !this.isMuted;
            console.log(this.isMuted)
            if (this.isMuted) {
                this.$refs.youtube.mute()
            } else {
                this.$refs.youtube.unMute()
            }
        },
        stateChange() {
            if (!this.$refs.youtube) return;
            let playerState = this.$refs.youtube.getPlayerState();
            this.isBuffering = playerState == 3;
            if (playerState != this.currentPlayerState && playerState == 1) { // If playing
                this.videoUpdateTimeInterval = setInterval(this.updateVideoTime, 100);
            } else {
                clearInterval(this.videoUpdateTimeInterval);
            }
            this.currentPlayerState = playerState;
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
            if (playerState == this.currentPlayerState || playerState == 1) clearInterval(this.videoUpdateTimeInterval)
            this.$emit('close');
        },
        calculateHoveredTimelineTime(e) {
            this.relativeMouseX = e.clientX - this.$refs.timeline.getBoundingClientRect().left;
            let timelineWidth = this.$refs.timeline.clientWidth;
            if (this.relativeMouseX < 0) {
                this.relativeMouseX = 0;
            } else if (this.relativeMouseX > timelineWidth) {
                this.relativeMouseX = timelineWidth;
            }
            this.videoTimeHovering = Math.floor(this.relativeMouseX / timelineWidth * this.video.durationSec);
            this.videoTimeHoveringFormatted = this.formatTimeSec(this.videoTimeHovering);
        },
        startDragTimeline() {
            this.playerStateBeforeDrag = this.$refs.youtube.getPlayerState();
            this.draggingType = 1;
            this.$refs.youtube.pauseVideo();
            this.seekToHoveredTime();
        },
        calculateVolumeSliderLevel(e) {
            let relativeVolMouseY = 1 - (e.clientY - this.$refs.volumeSlider.getBoundingClientRect().bottom);
            let volumeSliderHeight = this.$refs.volumeSlider.clientHeight;
            if (relativeVolMouseY < 0) {
                relativeVolMouseY = 0;
            } else if (relativeVolMouseY > volumeSliderHeight) {
                relativeVolMouseY = volumeSliderHeight;
            }
            this.volume = Math.floor(relativeVolMouseY / volumeSliderHeight * 100);
        },
        startDragVolumeSlider(e) {
            this.draggingType = 2;
            this.isMuted = false;
            this.$refs.youtube.unMute()
            this.calculateVolumeSliderLevel(e);
            this.$refs.youtube.setVolume(this.volume);
        },
        drag(e) {
            if (this.draggingType == 1) {
                this.calculateHoveredTimelineTime(e);
                this.seekToHoveredTime();
            } else if (this.draggingType == 2) {
                this.calculateVolumeSliderLevel(e);
                this.$refs.youtube.setVolume(this.volume);
            }
        },
        endDrag(e) {
            if (this.draggingType == 1) {
                if (this.playerStateBeforeDrag == 1 || this.playerStateBeforeDrag == 3) this.$refs.youtube.playVideo();
                this.playerStateBeforeDrag = null;
            } else if (this.draggingType == 2) {
                if (!this.isCursorInElement(e, this.$refs.volumeSliderOuterWrapper)) this.isVolumeWrapperOpen = false;
            }
            this.draggingType = 0;
        },
        mouseLeaveVolumeSliderWrapper() {
            if(this.draggingType != 2) this.isVolumeWrapperOpen = false
        },
        seekToHoveredTime() {
            this.setVideoTime(this.videoTimeHovering);
            this.$refs.youtube.seekTo(this.videoTimeHovering);
            this.stateChange();
        },
        gotoVideos() {
            if (this.isInFullscreenMode) this.toggleFullscreenMode();
            this.$router.push({
                name: 'Video\'s',
                path: '/videos'
            });
        },
        toggleFullscreenMode() {
            this.isInFullscreenMode = !this.isInFullscreenMode;
            let $player = this.$refs.videoPlayerWrapper;
            if (this.isInFullscreenMode) {
                if ($player.requestFullscreen) {
                    $player.requestFullscreen();
                } else if ($player.webkitRequestFullscreen) {
                    $player.webkitRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                }
            }
        },
        toggledFullscreen() {
            this.isInFullscreenMode = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement;
        },
        togglePlaybackRateModal() {
            this.isPlaybackRateModalOpen = !this.isPlaybackRateModalOpen;
        },
        setPlaybackRate(playbackRate) {
            this.playbackRate = playbackRate;
            this.$refs.youtube.setPlaybackRate(playbackRate);
        },
        resetIdleTimer() {
            this.clearIdleTimer();
            if (!this.isPaused && !this.isPlaybackRateModalOpen && this.isOnVideoPage) this.idleTimer = setTimeout(() => this.isIdle = true, 2000)
        },
        clearIdleTimer() {
            if (this.idleTimer) clearTimeout(this.idleTimer);
            this.isIdle = false;
        },
        clickAnywhere() {
            this.isPlaybackRateModalOpen = false;
        }
    },
    mounted() {
        document.addEventListener('fullscreenchange', this.toggledFullscreen, false);
        document.addEventListener('mozfullscreenchange', this.toggledFullscreen, false);
        document.addEventListener('MSFullscreenChange', this.toggledFullscreen, false);
        document.addEventListener('webkitfullscreenchange', this.toggledFullscreen, false);
        document.addEventListener('click', this.clickAnywhere, false);
    },
    unmounted() {
        document.removeEventListener('fullscreenchange', this.toggledFullscreen, false);
        document.removeEventListener('mozfullscreenchange', this.toggledFullscreen, false);
        document.removeEventListener('MSFullscreenChange', this.toggledFullscreen, false);
        document.removeEventListener('webkitfullscreenchange', this.toggledFullscreen, false);
        document.removeEventListener('click', this.clickAnywhere, false);
    },
    watch: {
        isOnVideoPage() {
            if (!this.isOnVideoPage) {
                this.setDimensionsMiniPlayer();
                this.isPlaybackRateModalOpen = false;
            }
        },
        video() {
            this.loadVideo();
        }
    }
}
</script>

<style lang="scss" scoped>
    @use "sass:math";
    @use '../mixins/scrim-gradient.scss' as *;
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
    }
    .videoPlayerWrapper.videoPage {
        .videoPlayer {
            position: absolute;
            width: 100%;
            top: 200px;
            left: 0;
            height: 100%;
            box-shadow: none;
            pointer-events: none;
    
            .playerContainer {
                position: absolute;
                left: calc(100% * #{math.div($containerMarginFrac, 2)} - 5px) !important;
                width: calc(100% * #{1 - $containerMarginFrac} - #{$videoPageSidebarWidth + $videoPageSpaceBetween - 10px}) !important;
                height: calc(100vw * #{math.div(1 - $containerMarginFrac, 16) * 9} - #{math.div($videoPageSidebarWidth + $videoPageSpaceBetween - 10px, 16) * 9 + 5px}) !important;
                pointer-events: auto;
    
                .clickToPause {
                    height: calc(100% - 60px);
                }
                .video {
                    border-radius: 4px;
                    &::after {
                        top: unset;
                        height: 100px;
                        @include scrimGradient(rgb(0, 0, 0), 'to top');
                    }
                }
                .youtube {
                    &, & > :first-child {
                        width: 600% !important;
                        height: 600% !important;
                    }
                    & > :first-child {
                        transform: translateX(-48.6%) translateY(-48.6%) scale(2.8%);
                    }
                }
                .overlay > button { display: none; }
            }
            .timeline {
                width: calc(100% - 20px);
                margin: 10px;
                transform: translateY(-500%);
                opacity: 0;
            }
            .playerContainer:not(.idle) {
                &.paused, &.pbrModalOpen {
                    .overlay, .video::after {
                        opacity: 1;
                    }
                }
                &:hover, &.dragging, &.paused, &.pbrModalOpen {
                    .timeline {
                        opacity: 1;
                    }
                }
            }
            .playerContainer.idle {
                .overlay, .video::after {
                    opacity: 0;
                }
                .clickToPause {
                    cursor: none;
                }
            }
            .title {
                display: none;
            }
        }

        &:fullscreen {
            .videoPlayer {
                top: 0;
            }
            .playerContainer {
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
            }
            .video .youtube {
                &, & > :first-child {
                    height: 600vh !important;
                    width: 600vw !important;
                }
                & > :first-child {
                    transform: translateX(-41.6%) translateY(-41.6%) scale(17%);
                }
            }
        }
    }
    .videoPlayerWrapper:not(.videoPage) {
        .volume {
            order: 3;
            margin: 0;
        }
        .volumeSliderOuterWrapper {
            left: unset;
            right: 1em;
            bottom: 20px;

            .muteAudio {
                bottom: 20px;
            }
        }
    }
    .playerContainer {
        &:hover, &.dragging {
            .video::after, .overlay { opacity: 1; }
        }
        &.paused .pauseIcon {
            opacity: 1;
            width: 70px;
            height: 70px;
        }
        &.buffering .loadingIcon {
            opacity: 1;
            width: 40px;
            height: 40px;
        }
    }
    .video {
        position: relative;
        height: 100%;
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
            margin-top: -2px;
            & > :first-child {
                height: 3000% !important;
                width: 3000% !important;
                transform: translateX(-48.33%) translateY(-48.33%) scale(3.335%);
            }
        }
        .overlay {
            position: absolute;
            opacity: 0;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
            z-index: 5;

            & > button {
                position: absolute;
                top: 20px;
                right: 20px;
            }
        }
        button {
            z-index: 8;

            &.expand {
                left: 20px;
                right: unset;
            }
        }
    }
    .statusIcon {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        transform: translateX(-50%) translateY(-50%);
        opacity: 0;
        z-index: 5;
        pointer-events: none;
        transition:
            opacity .3s cubic-bezier(.68,-0.55,.27,1.55),
            width .3s cubic-bezier(.68,-0.55,.27,1.55),
            height .3s cubic-bezier(.68,-0.55,.27,1.55);
    }
    .loadingIcon {
        border: 4px solid white;
        border-left-color: transparent;
        border-radius: 50%;
        top: 50px;
        right: 50px;
        left: unset;
        height: 0;
        animation: rotate 2s linear infinite;
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
    }
    .controls {
        display: flex;
        align-items: center;
        position: absolute;
        width: calc(100% - 40px);
        bottom: 10px;
        left: 20px;
        user-select: none;
        z-index: 7;

        .pausePlay, .volume {
            position: relative;
            margin-right: 20px;
        }
        .time {
            flex: 1;
            pointer-events: none;
            .currentTime {
                color: white;
            }
            .divider, .maxTime {
                color: rgb(204, 204, 204);
            }
        }
        .floatRight {
            align-self: flex-end;

            button {
                margin-left: 20px;
            }
        }
    }
    .volumeSliderOuterWrapper {
        position: absolute;
        width: 2em;
        height: 100px;
        bottom: 0;
        left: calc(2em + 20px);
        padding-bottom: 70px;
        z-index: 8;

        .volumeSliderInnerWrapper {
            background-color: rgba(41, 41, 41, .8);
            height: 100%;
            border-radius: 4px;
            cursor: pointer;
        }
        .volumeSlider {
            position: relative;
            width: 4px;
            height: 70%;
            background-color: rgba(200, 200, 200, 0.4);
            margin: auto;
            top: 50%;
            transform: translateY(-50%);
            border-radius: 4px;

            .volumeSliderLevel {
                position: absolute;
                background-color: $accentColor;
                width: 100%;
                height: 100%;
                border-radius: 4px;
                bottom: 0;

                &::after {
                    transform: none;
                    right: -2.5px;
                    top: -5px;
                }
            }
        }
        .muteAudio {
            position: absolute;
            bottom: 10px;
            background: transparent;
            border: none;
            z-index: 4;
            cursor: pointer;
            width: 100%;
            padding-bottom: 100%;
        }
    }
    .playbackRateModal {
        position: absolute;
        bottom: 60px;
        right: calc(4em - 10px);
        border-radius: 4px;
        overflow: hidden;
        z-index: 8;

        li {
            list-style: none;
            background-color: rgba(41, 41, 41, .8);
            color: white;
            flex: 1;
            padding: 10px 40px 10px 40px;
            font-size: .9em;
            text-align: center;
            user-select: none;
            cursor: pointer;

            &:hover {
                background-color: rgba(77, 77, 77, .8);
            }
            &.selected {
                color: $accentColor;
            }
        }
    }
    .clickToPause {
        position: absolute;
        height: 100%;
        width: 100%;
        top: 0;
        z-index: 6;
    }
    .timeline {
        position: absolute;
        width: 100%;
        height: 2px;
        padding: 6px 0;
        transform: translateY(-50%);
        cursor: pointer;
        z-index: 5;

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
        height: $miniPlayerTitleHeight;
        user-select: none;
        cursor: pointer;
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

    .timeline .currentTime::after, .volumeSliderLevel::after {
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
</style>