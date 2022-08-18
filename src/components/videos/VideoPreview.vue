<template>
    <router-link class="videoPreview" :to="{ name: 'Video', path: '/videos/:videoId/:videoPath', params: { videoId: video.id, videoPath: video.videoPath } }" :aria-label="video.title">
        <div class="thumb" :style="`background: linear-gradient(rgba(0, 0, 0, .1), rgba(0, 0, 0, .1)), url('${video.thumb}')`">
            <div class="foreground">
                <div class="expand" v-if="isPlaying">
                    <fa icon="external-link-alt" />
                </div>
                <div class="play" v-else>
                    <fa icon="play" />
                </div>
            </div>
        </div>
        <h4 class="title">
            {{video.title}}
        </h4>
    </router-link>
</template>

<script>
export default {
    name: 'VideoPreview',
    props: {
        video: Object,
        isPlaying: Boolean
    }
}
</script>

<style lang="scss" scoped>
    .videoPreview {
        display: inline-block;
        box-sizing: border-box;
        padding: 10px;
        cursor: pointer;

        &:hover, &:focus:focus-visible {
            .thumb {
                background-size: 110% !important;
            }
            .foreground {
                visibility: visible;
                svg {
                    opacity: 1;
                    transform: translateX(-50%) translateY(-50%);
                }
            }
        }
    }
    .thumb {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        background-size: 100% !important;
        background-position: center center !important;
        box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, .2);
        border-radius: 4px;
        overflow: hidden;
        transition: background-size .4s ease-in-out;
    }
    .foreground {
        position: absolute;
        display: block;
        visibility: hidden;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, .4);

        .expand {
            transform: rotate(270deg);
            height: 100%;
        }
        svg {
            position: absolute;
            top: 50%;
            left: 50%;
            color: white;
            font-size: 40px;
            opacity: 0;
            transform: translateX(-50%) translateY(-50%) scale(1.1);
            transition: opacity .2s ease-in-out,
                        transform .3s ease-in-out;
        }
    }
    .title {
        display: inline-block;
        color: $textColorGray;
        padding: 10px 10px;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
        font-size: .9em;
        font-weight: normal;
    }
</style>