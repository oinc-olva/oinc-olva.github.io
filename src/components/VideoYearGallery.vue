<template>
    <div class="videoYearGallery">
        <h2>{{schoolYear}}</h2>
        <div class="videoContent">
            <div class="video" :key="video" v-for="video in videos">
                <div class="thumb" :style="`background: linear-gradient(rgba(0, 0, 0, .3), rgba(0, 0, 0, .3)), url('${video.thumb}')`"></div>
                <h3 class="title">
                    {{video.title}}
                </h3>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VideoYearGallery',
    props: {
        schoolYear: String,
        videos: Array
    }
}
</script>

<style lang="scss" scoped>
    $videosPerLine: 4;

    .videoYearGallery {
        background-color: rgba(0, 0, 0, .1);
        padding: 10px;
        margin: 20px 0;
        border: 1px solid rgb(53, 53, 80);
        border-radius: 4px;

        h2 {
            position: relative;
            color: rgb(106, 105, 170);
            margin: 10px 0;
            text-align: center;
        }
    }
    .videoContent {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        padding: 0 20px;
    }
    .video {
        display: inline-block;
        box-sizing: border-box;
        padding: 10px;

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