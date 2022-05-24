<template>
    <div id="instagramVideo">
        <img v-if="!isVideoLoaded || isDisabled" :src="thumb" :alt="alt">
        <video v-if="!isDisabled" :src="media" ref="instagramVideoElement" @canplay="videoLoaded" @ended="videoEnded" @click="pauseVideo"></video>
        <img id="instagramVideoPauseIcon" :class="{'paused': isVideoPaused}" src="../../../assets/pause.svg" alt="Video gepauzeerd">
        <button id="instagramVideoSoundButton" class="icon" @click="muteVideo">
            <fa :icon="isVideoMuted ? 'volume-mute' : 'volume-up'" />
        </button>
    </div>
</template>

<script>
export default {
    name: 'InstagramVideo',
    props: {
        media: String,
        thumb: String,
        alt: String,
        isDisabled: Boolean
    },
    data() {
        return {
            isVideoLoaded: false,
            isVideoPaused: false,
            isVideoMuted: true
        }
    },
    methods: {
        videoLoaded() {
            this.isVideoLoaded = true;
            if (this.$refs.instagramVideoElement) {
                this.$refs.instagramVideoElement.muted = this.isVideoMuted;
                this.$refs.instagramVideoElement.volume = 1;
                this.$refs.instagramVideoElement.play();
            }
        },
        videoEnded() {
            this.$refs.instagramVideoElement.currentTime = 0;
            this.$refs.instagramVideoElement.play();
        },
        pauseVideo() {
            this.isVideoPaused = !this.isVideoPaused;
            if (this.isVideoPaused) {
                this.$refs.instagramVideoElement.pause();
            } else {
                this.$refs.instagramVideoElement.play();
            }
        },
        muteVideo() {
            this.isVideoMuted = !this.isVideoMuted;
            this.$refs.instagramVideoElement.muted = this.isVideoMuted;
        }
    }
}
</script>

<style lang="scss" scoped>
    #instagramVideo {
        position: relative;
    }
    img, video {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    #instagramVideoPauseIcon {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 70px;
        height: 70px;
        user-select: none;
        pointer-events: none;
        z-index: 5;
        opacity: 0;
        transform: translateX(-50%) translateY(-50%) scale(0);
        transition:
            opacity .3s cubic-bezier(.68,-0.55,.27,1.55),
            transform .3s cubic-bezier(.68,-0.55,.27,1.55);

        &.paused {
            opacity: 1;
            transform: translateX(-50%) translateY(-50%) scale(1);
        }
    }
    #instagramVideoSoundButton {
        position: absolute;
        z-index: 4;
        bottom: 20px;
        right: 20px;
        background-color: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 0, 0, 0.2);
        width: 30px;
        height: 30px;
        border-radius: 50%;

        svg {
            width: 50%;
        }
    }
</style>