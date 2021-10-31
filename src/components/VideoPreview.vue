<template>
    <div class="videoPreview" @click="open">
        <div class="thumb" :style="`background: linear-gradient(rgba(0, 0, 0, .1), rgba(0, 0, 0, .1)), url('${video.thumb}')`"></div>
        <h3 class="title">
            {{video.title}}
        </h3>
    </div>
</template>

<script>
export default {
    name: 'VideoPreview',
    props: {
        video: Object
    },
    methods: {
        open() {
            this.$router.push({
                name: 'Video',
                path: '/videos/:videoId/:videoName',
                params: {
                    videoId: this.video.id,
                    videoName: this.video.videoPath
                }
            })
        }
    }
}
</script>

<style lang="scss" scoped>
    .videoPreview {
        display: inline-block;
        box-sizing: border-box;
        padding: 10px;
        cursor: pointer;

        &:hover .thumb {
            background-size: 110% !important;
        }
    }
    .thumb {
        width: 100%;
        padding-top: 56.25%;
        background-size: 100% !important;
        background-position: center center !important;
        box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, .2);
        border-radius: 4px;
        transition: all .4s ease-in-out;
    }
    .title {
        color: rgb(131, 131, 131);
        font-weight: normal;
        font-size: .9em;
        padding: 5px 10px;
        border-radius: 4px;
    }
</style>