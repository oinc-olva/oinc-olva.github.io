<template>
    <div id="videoPlayerWrapper" ref="videoPlayerWrapper" :class="{videoPage: isOnVideoPage}">
        <div class="dragOverlay" v-if="draggingType != 0" @mousemove="drag" @mouseup="endDrag" />
        <div id="videoPlayer" v-if="video" @dragstart="preventDefault" aria-label="Videospeler">
            <div id="playerContainer" :class="{dragging: draggingType != 0, paused: isPaused, buffering: isBuffering, pbrModalOpen: isPlaybackRateModalOpen, idle: isIdle}">
                <div id="playerContent" v-show="errorVal == 0" @mouseenter="resetIdleTimer" @mouseleave="clearIdleTimer">
                    <div id="video" ref="video" v-on="{ click: isOnVideoPage ? null : () => pausePlay(false)}">
                        <YouTube id="youtube" ref="youtube" v-show="errorVal == 0" :vars="playerVars" :width="videoWidth" :height="videoHeight" src="" @ready="loadVideo" @state-change="stateChange" @error="error" draggable="false" />
                        <div class="overlay">
                            <button class="close icon" tabindex="3" aria-label="Afsluiten" @click.stop="close"><fa icon="times" /></button>
                            <button class="expand icon" tabindex="2" aria-label="Vergroten" @click.stop="expand"><fa icon="external-link-alt" rotation="270" /></button>
                            <div class="controls">
                                <button class="pausePlay icon" tabindex="6" :aria-label="currentPlayerState == 0 ? 'Herhalen' : (isPaused ? 'Afspelen' : 'Pauzeren')" @click.stop="currentPlayerState == 0 ? replay() : pausePlay(false)"><fa :icon="currentPlayerState == 0 ? 'rotate-left' : (isPaused ? 'play' : 'pause')" /></button>
                                <button class="volume icon" tabindex="-1" aria-label="Volume" @mouseover="this.isVolumeWrapperOpen = true"><fa :icon="this.isMuted ? 'volume-mute' : (this.volume == 0 ? 'volume-off' : (this.volume < 70 ? 'volume-down' : 'volume-up'))" /></button>
                                <div id="time" v-if="$refs.youtube">
                                    <span id="currentTime">{{videoTimeSecFormatted}}</span>
                                    <span id="divider"> / </span>
                                    <span id="maxTime">{{video.durationFormatted}}</span>
                                </div>
                                <div class="floatRight" v-if="isOnVideoPage">
                                    <button class="youtubeBtn icon" tabindex="9" aria-label="Op YouTube bekijken" @click.stop="watchOnYoutube"><fa :icon="['fab', 'youtube']" /></button>
                                    <button class="playbackRate icon" tabindex="9" ref="playbackRateBtn" aria-label="Snelheid" @click.stop="togglePlaybackRateModal"><fa icon="tachometer-alt" /></button>
                                    <button class="miniplayer icon" tabindex="11" aria-label="Minimalizeren" @click="gotoVideos"><fa icon="external-link-alt" rotation="90" /></button>
                                    <button class="fullscreen icon" tabindex="11" aria-label="Volledig scherm" @click="toggleFullscreenMode"><fa :icon="this.isInFullscreenMode ? 'compress' : 'expand'" /></button>
                                </div>
                            </div>
                        </div>
                        <div id="idleOverlay" @mousemove="resetIdleTimer" @click="() => pausePlay(true)" aria-hidden="true"></div>
                        <div id="status">
                            <img id="pauseIcon" class="statusIcon" src="../../assets/pause.svg" alt="Video Paused">
                            <div id="bufferingIcon" class="statusIcon" />
                        </div>
                    </div>
                    <div id="volumeSliderOuterWrapper" :class="{open: isVolumeWrapperOpen}" ref="volumeSliderOuterWrapper" @mouseleave="mouseLeaveVolumeSliderWrapper">
                        <div id="volumeSliderInnerWrapper" tabindex="8" @mousedown.left="startDragVolumeSlider" @keydown="sliderVolumeKeydown" role="slider" aria-label="volume" aria-valuemin="0" aria-valuemax="100" :aria-valuenow="volume" :aria-valuetext="`${this.volume}%`">
                            <div id="volumeSlider" ref="volumeSlider">
                                <div id="volumeSliderLevel" :style="{height: this.isMuted ? '0' : this.volume + '%'}" />
                            </div>
                        </div>
                        <button class="muteAudio icon" tabindex="7" :aria-label="isMuted ? 'Geluid inschakelen' : 'Geluid uitschakelen'" @click="toggleMute"></button>
                    </div>
                    <div id="playbackRateModal" ref="playbackRateModal" v-show="isPlaybackRateModalOpen" @keydown.esc.stop="togglePlaybackRateModal">
                        <ul role="listbox" aria-label="Snelheid kiezen">
                            <li :key="option" v-for="option in availablePlaybackRates" :class="{selected: this.playbackRate == option}" tabindex="10" @click="setPlaybackRate(option)" @keydown.enter.space.prevent="setPlaybackRate(option)" role="option" :aria-label="option == 1 ? 'originele snelheid' : `${option*100}% van originele snelheid`" :aria-selected="this.playbackRate == option">{{option}}</li>
                        </ul>
                    </div>
                    <div id="timeline" :tabindex="this.isOnVideoPage ? 5 : 12" :class="{dragging: this.draggingType == 1}" ref="timeline" @mousemove="calculateHoveredTimelineTime" @mousedown.left="startDragTimeline" @keydown="sliderTimelineKeydown" role="slider" aria-label="tijdlijn" aria-valuemin="0" :aria-valuemax="video.durationSec" :aria-valuenow="videoTimeSec" :aria-valuetext="timelineAriaText">
                        <div id="tlBackground"></div>
                        <div id="tlBuffered" :style="{width: this.videoLoadedFrac * 100 + '%'}"></div>
                        <div id="tlProgress" :style="{width: this.videoTimeSec / this.video.durationSec * 100 + '%'}"></div>
                        <div id="tlHoverTimeTooltip" :style="{left: this.relativeMouseX + 'px'}">{{this.videoTimeHoveringFormatted}}</div>
                    </div>
                </div>
                <EndScreen v-if="currentPlayerState == 0" :videos="videos" :recommendedVideoIds="recommendedVideoIds" :isAutoplay="isAutoplay" :isOnVideoPage="isOnVideoPage" @setCurrentVideoId="videoId => $emit('setCurrentVideoId', videoId)" />
                <div id="error" v-if="errorVal != 0">
                    <div class="overlay">
                        <button class="close icon" aria-label="Afsluiten" @click.stop="close"><fa icon="times" /></button>
                        <button class="expand icon" aria-label="Vergroten" @click.stop="expand"><fa icon="external-link-alt" rotation="270" /></button>
                    </div>
                    <div id="errorContent">
                        <h2>Het lijkt erop dat de video niet kan geladen worden!</h2>
                        <div id="errorReason">
                            <p v-if="errorVal == 2">Deze video bestaat niet.</p>
                            <p v-if="errorVal == 5">De videospeler heeft een onbekende error opgetreden. Probeer de pagina te herladen.</p>
                            <p v-if="errorVal == 100">Deze video is privé of verwijderd.</p>
                            <p v-if="errorVal == 101 || errorVal == 150">Probeer deze video te bekijken op YouTube.</p>
                        </div>
                    </div>
                    <div class="controls" v-if="isOnVideoPage">
                        <span id="errorNum">Error {{errorVal}}</span>
                        <div class="floatRight">
                            <button class="miniplayer icon" aria-label="Minimalizeren" @click="gotoVideos"><fa icon="external-link-alt" rotation="90" /></button>
                            <button class="watchOnYoutube icon" aria-label="Op YouTube bekijken" @click="watchOnYoutube"><fa :icon="['fab', 'youtube']" /></button>
                            <a class="watchOnYoutube btn" :href="`https://www.youtube.com/watch?v=${this.video.id}`" target="_blank">Op YouTube bekijken</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import YouTube from 'vue3-youtube';
import EndScreen from './EndScreen.vue';

export default {
    name: 'VideoPlayer',
    components: {
        YouTube,
        EndScreen
    },
    props: {
        video: Object,
        playerPlaylistInfo: Object,
        videos: Object,
        recommendedVideoIds: Array,
        isAutoplay: Boolean,
        isOnVideoPage: Boolean
    },
    emits: [
        'close',
        'setCurrentVideoId'
    ],
    data() {
        return {
            videoWidth: 100,
            videoHeight: 100,
            videoTimeSec: 0,
            videoTimeSecFormatted: '0:00',
            timelineAriaText: '',
            videoTimeHovering: 0,
            videoTimeHoveringFormatted: '0:00',
            errorVal: 0,
            volume: 100,
            isMuted: false,
            relativeMouseX: 0,
            videoLoadedFrac: 0,
            videoUpdateTimeInterval: null,
            isVolumeWrapperOpen: false,
            currentPlayerState: -1,
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
                hl: 'nl',
                cc_lang_pref: 'nl',
                controls: 0
            }
        }
    },
    methods: {
        preventDefault(e) {
            e.preventDefault();  
        },
        loadVideo() {
            this.$refs.youtube.loadVideoById(this.video.id);
            this.$refs.youtube.playVideo();
            this.$refs.video.firstChild.firstChild.setAttribute('tabindex', -1);
            this.$refs.video.firstChild.firstChild.setAttribute('aria-hidden', 'true');
            this.isPaused = false;
            this.errorVal = 0;
            if (!this.isOnVideoPage) this.setDimensionsMiniPlayer();
        },
        replay() {
            this.setVideoTime(0);
            this.$refs.youtube.playVideo();
            this.isPaused = false;
            this.resetIdleTimer();
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
        getTimelineAriaText(secFormatted) {
            let secFormattedSplit = secFormatted.split(':');
            if (secFormattedSplit.length == 2) secFormattedSplit.unshift('0');

            const TR = ['uur', 'uren', 'minuut', 'minuten', 'seconde', 'seconden'];
            let translation = [];
            for (let i = 0; i < secFormattedSplit.length; i++) {
                const val = parseInt(secFormattedSplit[i], 10);
                if (val == 0) {
                    continue;
                } else if (val == 1) {
                    translation.push('1 ' + TR[i*2]);
                } else {
                    translation.push(val + ' ' + TR[i*2+1]);
                }
            }
            return translation.join(' ') + ' van ' + this.video.durationTranslated;
        },
        isCursorInElement(e, $el) {
            let rect = $el.getBoundingClientRect();
            return e.clientY > rect.top && e.clientY < rect.bottom && e.clientX > rect.left && e.clientX < rect.right;
        },
        pausePlay(isResetIdleTimer) {
            if (this.isPlaybackRateModalOpen) {
                this.isPlaybackRateModalOpen = false;
                this.resetIdleTimer();
                return;
            }
            let playerState = this.$refs.youtube.getPlayerState();
            if (playerState == -1 || playerState == 2) { // Als nog niet gestart of gepauzeerd
                this.$refs.youtube.playVideo();
                this.isPaused = false;
                if (isResetIdleTimer) this.resetIdleTimer();
            } else if (playerState == 1) { // Als aan het afspelen
                this.$refs.youtube.pauseVideo();
                this.isPaused = true;
                this.clearIdleTimer();
            }
        },
        toggleMute() {
            this.isMuted = !this.isMuted;
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
            if (playerState != this.currentPlayerState) {
                let prevPlayerState = this.currentPlayerState;
                this.currentPlayerState = playerState; // Update afspeelstatus
                
                if (playerState == 1) { // Als nu aan het afspelen...
                    if (prevPlayerState == 2) this.resetIdleTimer(); // Als vooraf gepauzeerd, reset idle timer (zodat cursor na tijdje weer verdwijnt)
                    this.videoUpdateTimeInterval = setInterval(this.updateVideoTime, 100);
                    this.isPaused = false;
                } else { // Anders...
                    clearInterval(this.videoUpdateTimeInterval); // Pauzeer het updaten van de verstreken videotijd in de navigatiebalk onderaan
                    if (playerState == 2 && this.draggingType != 1) { // Als nu gepauzeerd...
                        this.isPaused = true;
                        this.clearIdleTimer();
                    } else if (playerState == 0) { // Als de video beëindigd wordt
                        this.setVideoTime(this.video.durationSec); // Ga naar einde van video
                        
                        // Als er een afspeellijst actief is en er een volgende video is genomen...
                        if (this.playerPlaylistInfo.playlistId != '' && this.playerPlaylistInfo.nextVideoId != '') {
                            this.currentPlayerState = -1;
                            if (this.$route.name == 'Video') {
                                this.$router.push({
                                    name: 'Video',
                                    path: '/videos/:videoId/:videoPath',
                                    params: {
                                        videoId: this.playerPlaylistInfo.nextVideoId,
                                        videoPath: this.videos.values[this.playerPlaylistInfo.nextVideoId].videoPath
                                    },
                                    query: {
                                        lijst: this.playerPlaylistInfo.playlistId
                                    }
                                });
                            } else {
                                this.$emit('setCurrentVideoId', this.playerPlaylistInfo.nextVideoId)
                            }
                        }
                    }
                }
            }
        },
        updateVideoTime() {
            this.setVideoTime(this.$refs.youtube.getCurrentTime());
        },
        setVideoTime(timeSec) {
            let prevVideoTimeSec = this.videoTimeSec;
            this.videoTimeSec = Math.floor(timeSec);
            this.videoLoadedFrac = this.$refs.youtube.getVideoLoadedFraction();
            if (prevVideoTimeSec != this.videoTimeSec) {
                this.videoTimeSecFormatted = this.formatTimeSec(this.videoTimeSec);
                this.timelineAriaText = this.getTimelineAriaText(this.videoTimeSecFormatted)
            }
        },
        expand() {
            this.$router.push({
                name: 'Video',
                path: '/videos/:videoId/:videoPath',
                params: {
                    videoId: this.video.id,
                    videoPath: this.video.videoPath
                },
                query: {
                    lijst: this.playerPlaylistInfo.playlistId
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
            if (this.draggingType == 1) { // Tijdlijn
                this.calculateHoveredTimelineTime(e);
                this.seekToHoveredTime();
            } else if (this.draggingType == 2) { // Volume
                this.calculateVolumeSliderLevel(e);
                this.$refs.youtube.setVolume(this.volume);
            }
        },
        endDrag(e) {
            if (this.draggingType == 1) { // Tijdlijn
                if (this.playerStateBeforeDrag == 1 || this.playerStateBeforeDrag == 3) this.$refs.youtube.playVideo();
                this.playerStateBeforeDrag = null;
            } else if (this.draggingType == 2) { // Volume
                if (!this.isCursorInElement(e, this.$refs.volumeSliderOuterWrapper)) this.isVolumeWrapperOpen = false;
            }
            this.draggingType = 0;
        },
        mouseLeaveVolumeSliderWrapper() {
            if(this.draggingType != 2) this.isVolumeWrapperOpen = false; // Als de volumebalk niet wordt gebruikt, laat het verdwijnen
        },
        sliderVolumeKeydown(e) {
            let prevVolume = this.volume;
            if (e.key == 'ArrowLeft' || e.key == 'ArrowDown') {
                this.volume -= 5;
                if (this.volume < 0) this.volume = 0;
                e.preventDefault();
            }
            if (e.key == 'ArrowRight' || e.key == 'ArrowUp') {
                this.volume += 5;
                if (this.volume > 100) this.volume = 100;
                e.preventDefault();
            }

            if (this.volume != prevVolume) {
                if (this.isMuted) this.toggleMute();
                this.$refs.youtube.setVolume(this.volume);
            }            
        },
        sliderTimelineKeydown(e) {
            let prevTimeSec = this.videoTimeSec;
            if (e.key == 'ArrowLeft' || e.key == 'ArrowDown') {
                this.videoTimeSec -= 5;
                if (this.videoTimeSec < 0) this.videoTimeSec = 0;
                e.preventDefault();
            }
            if (e.key == 'ArrowRight' || e.key == 'ArrowUp') {
                this.videoTimeSec += 5;
                if (this.videoTimeSec > this.video.durationSec) this.videoTimeSec = this.video.durationSec;
                e.preventDefault();
            }

            if (this.videoTimeSec != prevTimeSec) {
                this.setVideoTime(this.videoTimeSec);
                this.$refs.youtube.seekTo(this.videoTimeSec);
                this.videoTimeSecFormatted = this.formatTimeSec(this.videoTimeSec);
                this.stateChange();
            }
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
            if (!this.isInFullscreenMode) document.activeElement.blur();
        },
        togglePlaybackRateModal() {
            this.isPlaybackRateModalOpen = !this.isPlaybackRateModalOpen;
            this.availablePlaybackRates = this.$refs.youtube.getAvailablePlaybackRates();
            if (this.isPlaybackRateModalOpen) {
                this.$nextTick(() => {
                    this.$refs.playbackRateModal.getElementsByClassName('selected')[0].focus();
                });
            } else {
                this.$refs.playbackRateBtn.focus();
            }
        },
        setPlaybackRate(playbackRate) {
            this.playbackRate = playbackRate;
            this.$refs.youtube.setPlaybackRate(playbackRate);
        },
        resetIdleTimer() {
            this.clearIdleTimer();
            if (!this.isPaused && !this.isPlaybackRateModalOpen && this.isOnVideoPage) this.idleTimer = setTimeout(() => this.isIdle = true, 3200)
        },
        clearIdleTimer() {
            if (this.idleTimer) clearTimeout(this.idleTimer);
            this.isIdle = false;
        },
        clickAnywhere() {
            this.isPlaybackRateModalOpen = false;
        },
        error(err) {
            this.errorVal = err.data;
            console.error(`Kon de video met id '${this.video.id}' niet laden (met error ${this.errorVal})`);
        },
        watchOnYoutube() {
            window.open('https://www.youtube.com/watch?v=' + this.video.id, '_blank');
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
    @use '../../mixins/scrim-gradient.scss' as *;

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .dragOverlay {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        cursor: pointer;
        z-index: 20;
    }
    #videoPlayerWrapper.videoPage {
        #videoPlayer {
            position: absolute;
            width: 100%;
            top: 200px;
            left: 0;
            height: 100%;
            box-shadow: none;
            pointer-events: none;
            animation-name: fadeIn;
            animation-duration: 1s;
            animation-fill-mode: both;
            animation-delay: .6s;
    
            #playerContainer {
                position: absolute;
                left: var(--pcLeft) !important;
                width: var(--pcWidth) !important;
                height: var(--pcHeight) !important;
                pointer-events: auto;

                #playerContent { height: 100%; }    
                #video {
                    border-radius: 4px;
                    &::after { display: none; }

                    & > .overlay { transition: opacity .1s ease-in-out; }
                }
                #youtube {
                    &, & > :first-child {
                        width: 100% !important;
                        height: 100% !important;
                    }
                }
                #error {
                    animation-name: fadeIn;
                    animation-duration: 1s;

                    #errorContent { transform: translateY(calc(-50% - 30px)); }
                }
                .overlay {
                    & > button { display: none; }
                    & > .controls {
                        &::before {
                            content: '';
                            position: absolute;
                            bottom: 0;
                            left: 0;
                            height: 100px;
                            width: 100%;
                            pointer-events: none;
                            @include scrimGradient(rgb(0, 0, 0), 'to top');
                        }
                        &::after {
                            content: '';
                            display: block;
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            backdrop-filter: blur(1px);
                            z-index: -1;
                        }
                    }
                }
            }
            #timeline {
                width: calc(100% - 20px);
                margin: 10px;
                transform: translateY(-500%);
                opacity: 0;
                transition: opacity .1s ease-in-out;
            }
            #playerContainer:not(.idle) {
                &.paused, &.pbrModalOpen {
                    .overlay, #video::after {
                        opacity: 1;
                    }
                }
                &:hover, &.dragging, &.paused, &.pbrModalOpen, &:focus-within {
                    #timeline {
                        opacity: 1;
                    }
                }
            }
            #playerContainer.idle:not(:focus-within) {
                cursor: none;

                .overlay, #video::after { opacity: 0; }
                #idleOverlay {
                    position: absolute;
                    top: 0;
                    right: 0;
                    bottom: 0;
                    left: 0;
                    z-index: 10;
                }
            }
            #playerContainer.idle:focus-within {
                #timeline { opacity: 1; }
            }
        }

        &:fullscreen {
            #videoPlayer {
                top: 0;

                #playerContainer {
                    left: 0 !important;
                    width: 100vw !important;
                    height: 100vh !important;
                }
            }
        }
    }
    #videoPlayerWrapper:not(.videoPage) {
        position: relative;

        .volume {
            order: 3;
            margin: 0;
        }
        #volumeSliderOuterWrapper {
            left: unset;
            right: 1em;
            bottom: -20px;

            .muteAudio {
                bottom: 30px;
            }
        }
    }
    #endScreen {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        border-radius: 4px;
    }
    #error {
        position: relative;
        width: 100%;
        height: 100%;
        background-color: $videoBackground;
        border-radius: 4px;
        color: white;
        overflow: hidden;

        #errorContent {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 100%;
            padding: 0 10%;
            text-align: center;
            box-sizing: border-box;

            h2 { font-size: 1.5rem; }
            #errorReason {
                color: rgb(150, 150, 150);
                margin-top: 20px;
            }
        }
        .controls {
            justify-content: space-between;
            padding: 30px 40px;

            #errorNum { color: gray; }
            button {
                position: relative;
                z-index: 10;
                
                &.miniplayer { margin-right: 20px; }
                &.watchOnYoutube.icon {
                    display: none;

                    &::before { right: 60px; }
                }
            }
            a.watchOnYoutube.btn {
                margin-left: 20px;
            }
        }
    }
    #playerContainer {
        background-color: #1a1d25;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;

        &:hover, &.dragging, &:focus-within {
            #video::after, .overlay { opacity: 1; }
        }
        &.paused #pauseIcon {
            opacity: 1;
            width: 70px;
            height: 70px;
            user-select: none;
        }
        &.buffering #bufferingIcon {
            opacity: 1;
            width: 40px;
            height: 40px;
        }
    }
    #video {
        position: relative;
        height: 100%;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        overflow: hidden;

        &::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, .5);
            opacity: 0;
            transition: opacity .1s ease-in-out;
        }

        #youtube {
            margin-top: 0;
            margin-bottom: -5px;
            & > :first-child { user-select: none; }
        }
        button {
            z-index: 8;
            position: relative;
        }
    }
    #videoPlayer .overlay {
        position: absolute;
        opacity: 0;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 5;
        pointer-events: none;

        .controls { pointer-events: all; }
        & > button.icon {
            position: absolute;
            top: 20px;
            right: 20px;
            pointer-events: all;

            &.expand {
                left: 20px;
                right: unset;
            }
        }
    }
    #status {
        user-select: none;
        pointer-events: none;
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
    #bufferingIcon {
        border: 4px solid white;
        border-left-color: transparent;
        border-radius: 50%;
        height: 0;
        animation: rotate 2s linear infinite;
            @keyframes rotate {
                from { transform: translateX(-50%) translateY(-50%) rotate(0deg); }
                to { transform: translateX(-50%) translateY(-50%) rotate(360deg); }
            }
    }
    .controls {
        display: flex;
        align-items: center;
        position: absolute;
        width: 100%;
        bottom: 0;
        left: 0;
        padding: 10px 20px;
        box-sizing: border-box;
        user-select: none;
        z-index: 7;

        .pausePlay, .volume {
            position: relative;
            margin-right: 20px;
        }
        #time {
            flex: 1;
            pointer-events: none;
            z-index: 1;

            #currentTime {
                color: white;
            }
            #divider, #maxTime {
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
    #volumeSliderOuterWrapper {
        position: absolute;
        width: 2em;
        height: 100px;
        bottom: 0;
        left: calc(2em + 20px);
        padding-bottom: 70px;
        opacity: 0;
        pointer-events: none;
        z-index: 8;

        &.open, &:focus-within {
            opacity: 1;
            pointer-events: all;
        }

        #volumeSliderInnerWrapper {
            background-color: rgba(41, 41, 41, .9);
            height: 100%;
            border-radius: 4px;
            cursor: pointer;
        }
        #volumeSlider {
            position: relative;
            width: 4px;
            height: 70%;
            background-color: rgba(200, 200, 200, 0.4);
            margin: auto;
            top: 50%;
            transform: translateY(-50%);
            border-radius: 4px;

            #volumeSliderLevel {
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
    button.icon:not(.muteAudio) {
        &::before {
            content: attr(aria-label);
            position: absolute;
            font-size: .8em;
            right: 50%;
            transform: translateX(50%);
            bottom: 35px;
            background: #21242e;
            padding: 4px 8px;
            margin-bottom: 20px;
            opacity: 0;
            pointer-events: none;
            z-index: 7;
            border-radius: 4px;
            white-space: nowrap;
            transition: opacity .2s ease-in-out;
        }
        &:hover::before, &:focus:focus-visible:before {
            opacity: 1;
        }

        &.expand::before, &.close::before {
            bottom: unset;
            top: 40px;
        }
    }
    button.pausePlay::before, button.icon.expand::before { left: -300%; right: unset !important; }
    button.icon.fullscreen::before, button.icon.close::before { transform: none; right: -8px }
    #videoPlayerWrapper:not(.videoPage) {
        .pausePlay::before, .muteAudio::before {
            bottom: 20px;
        }
        #error {
            height: 225px;
        }
    }
    #playbackRateModal {
        position: absolute;
        bottom: 60px;
        right: calc(4em - 10px);
        z-index: 6;

        li {
            position: relative;
            list-style: none;
            background-color: rgba(41, 41, 41, .9);
            color: white;
            padding: 10px 40px 10px 40px;
            font-size: .9em;
            text-align: center;
            user-select: none;
            cursor: pointer;
            transition: background-color .1s ease-in-out;

            &:hover, &:not(.selected):focus:focus-visible {
                background-color: rgba(63, 63, 63, .9);
            }
            &:focus:focus-visible { z-index: 3; }
            &.selected {
                color: $accentColor;
                font-weight: bold;
                z-index: 2;
                background-color: rgba(85, 85, 85, .9);

                &::before {
                    content: '';
                    display: inline-block;
                    position: absolute;
                    left: 0;
                    top: 0;
                    height: 100%;
                    width: 4px;
                    border-radius: 4px;
                    background-color: $accentColor;
                }
            }

            &:first-child {
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            &:last-child {
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 4px;
            }
        }
    }
    #timeline {
        position: absolute;
        width: 100%;
        height: 2px;
        padding: 6px 0;
        transform: translateY(-50%);
        cursor: pointer;
        z-index: 5;

        &:hover, &.dragging {
            #tlBackground, #tlBuffered, #tlProgress {
                height: 5px;
                transform: translateY(-3px);
            }
            #tlProgress::after { transform: scale(1); }
            #tlHoverTimeTooltip { opacity: 1; }
        }

        #tlBackground, #tlBuffered, #tlProgress {
            position: absolute;
            left: 0;
            top: 50%;
            height: 2px;
            background-color: rgba(200, 200, 200, .3);
            transition: 
                height .1s ease-in-out,
                transform .1s ease-in-out;
        }
        #tlBackground { width: 100%; }
        #tlProgress {
            position: relative;
            background-color: rgb(85, 199, 228);
        }
        #tlHoverTimeTooltip {
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

    #timeline #tlProgress::after, #volumeSliderLevel::after {
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

    // (Her)schaling van video op videopagina
    #videoPlayerWrapper.videoPage #playerContainer {
        --pcLeft: calc(100% * #{math.div($containerMarginFrac, 2)} - 5px) !important;
        --pcWidth: calc(100% * #{1 - $containerMarginFrac - $videoPageSidebarWidthFrac} - #{$videoPageSpaceBetween - 10px}) !important;
        --pcHeight: calc(100vw * #{math.div(1 - $containerMarginFrac - $videoPageSidebarWidthFrac, 16) * 9} - #{math.div($videoPageSpaceBetween - 10px, 16) * 9 + 5px}) !important;
    }
    @media screen and (max-width: $videoPageRescale1Viewport) {
        #videoPlayerWrapper.videoPage #playerContainer {
            --pcLeft: calc(100% * #{math.div(1 - $videoPageRescale1WidthFrac, 2)} - 5px) !important;
            --pcWidth: calc(100% * #{$videoPageRescale1WidthFrac} + 13px) !important;
            --pcHeight: calc(100vw * #{math.div($videoPageRescale1WidthFrac, 16) * 9}) !important;
        }
    }
    @media screen and (max-width: $videoPageRescale2Viewport) {   
        #videoPlayerWrapper.videoPage {
            #videoPlayer {
                top: 140px;
            }
            #playerContainer {
                --pcLeft: calc(100% * #{math.div(1 - $videoPageRescale2WidthFrac, 2)} - 7px) !important;
                --pcWidth: calc(100% * #{$videoPageRescale2WidthFrac} + 13px) !important;
                --pcHeight: calc(100vw * #{math.div($videoPageRescale2WidthFrac, 16) * 9}) !important;
            }
            #errorContent {
                h2 { font-size: 3.5vw; }
                #errorReason { font-size: 2.5vw; }
            }
        }
    }
    @media screen and (max-width: 580px) {
        #videoPlayerWrapper.videoPage #error .controls {
            padding: 12px;

            #errorNum { font-size: .8em; }
            button.btn { font-size: .7em; }
            button.miniplayer, button.watchOnYoutube.icon {
                font-size: 1em;
                margin-right: 10px;
            }
        }
    }
    @media screen and (max-width: 440px) {
        #videoPlayerWrapper:not(.videoPage) {
            #youtube {
                width: calc(100vw - 24px) !important;
                height: calc((100vw - 24px) / 16 * 9) !important;

                & > :first-child {
                    width: 100% !important;
                    height: 100% !important;
                }
            }
            #playerContainer.paused #pauseIcon {
                width: 15vw;
            }
        }
        #videoPlayerWrapper.videoPage #videoPlayer #playerContainer #error {
            #errorContent {
                transform: translateY(-50%);

                h2 { font-size: 1em; }
                #errorReason { font-size: .8em; }
            }
            .controls {
                justify-content: right;
                left: unset;
                right: 5px;
                bottom: 5px;

                #errorNum, .watchOnYoutube.btn { display: none; }
                button.watchOnYoutube.icon, button.miniplayer {
                    display: inline-block;
                    margin-left: 10px;
                    margin-right: 10px;
                }
            }
        }
    }
    @media screen and (max-width: 410px) {
        #videoPlayerWrapper.videoPage #videoPlayer #playerContainer {
            #timeline {
                transform: translateY(-450%);
            }
            .overlay .controls {
                button.icon, #time span {
                    font-size: 15px;
                }
                button.icon::before {
                    bottom: 25px;
                }
                & > button.icon {
                    margin-right: 15px;
                }
                .floatRight {
                    margin-left: 15px;
                }
            }
            #clickToPause {
                height: calc(100% - 50px);
            }
            #volumeSliderOuterWrapper {
                left: calc(2em + 6px);
            }
        }
    }
    @media screen and (max-width: 390px) {
        #videoPlayerWrapper.videoPage #videoPlayer .controls #time {
            #divider, #maxTime {
                display: none;
            }
        }
    }
</style>