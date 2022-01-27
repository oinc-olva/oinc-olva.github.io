<template>
    <div class="videoYearGallery">
        <h2>{{schoolYear}}</h2>
        <div class="videoContent">
            <VideoPreview class="video" :key="video" v-for="video in videos" :video="video" :isPlaying="playerVideo ? video.id == playerVideo.id : false" />
        </div>
    </div>
</template>

<script>
import VideoPreview from './VideoPreview.vue'

export default {
    name: 'VideoYearGallery',
    components: {
        VideoPreview
    },
    props: {
        schoolYear: String,
        videos: Array,
        playerVideo: Object
    }
}
</script>

<style lang="scss" scoped>
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
        grid-template-columns: repeat( auto-fill, minmax(calc(120px + 6vw), 1fr) );
        padding: 0 20px;
    }
</style>