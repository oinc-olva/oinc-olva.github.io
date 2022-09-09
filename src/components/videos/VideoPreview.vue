<template>
    <router-link class="videoPreview" :to="{ name: 'Video', path: '/videos/:videoId/:videoPath', params: { videoId: video.id, videoPath: video.videoPath } }" :aria-label="video.title">
        <div class="thumb">
            <div class="thumbInnerWrapper" :style="`background: linear-gradient(rgba(0, 0, 0, .1), rgba(0, 0, 0, .1)), url('${video.thumb}')`">
                <div class="foreground">
                    <div class="expand" v-if="isPlaying">
                        <fa icon="external-link-alt" />
                    </div>
                    <div class="play" v-else>
                        <fa icon="play" />
                    </div>
                </div>
            </div>
        </div>
        <component :is="`h${headingLevel}`" class="title">
            {{video.title}}
        </component>
    </router-link>
</template>

<script>
export default {
    name: 'VideoPreview',
    props: {
        headingLevel: {
            type: Number,
            default: 4
        },
        video: Object,
        isPlaying: Boolean
    }
}
</script>

<style lang="scss" scoped>
    .videoPreview {
        display: inline-block;
        box-sizing: border-box;
        text-align: center;
        padding: 10px;
        cursor: pointer;

        &:hover, &:focus:focus-visible {
            .thumbInnerWrapper {
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
        display: flex;
        position: relative;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        border-radius: 4px;
        overflow: hidden;
    }
    .thumbInnerWrapper {
        position: relative;
        width: 100%;
        padding-top: 56.25%;
        background-size: 100% !important;
        background-position: center center !important;
        transition: background-size .4s ease-in-out;
    }
    .foreground {
        position: absolute;
        display: block;
        visibility: hidden;
        top: 0;
        width: 100%;
        height: 100%;
        box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, .2);
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
        display: flex;
        position: relative;
        flex-direction: column;
        justify-content: center;
        color: $textColorGray;
        padding: 10px 10px;
        width: 100%;
        box-sizing: border-box;
        font-size: .9em;
        font-weight: normal;
    }
</style>