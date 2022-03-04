<template>
    <div class="videoYearGallery" ref="videoYearGallery">
        <h3>{{schoolYear}}</h3>
        <ul class="videoContent" :aria-label="`Videos van schooljaar ${schoolYear}`">
            <li class="videoItem" :key="video" v-for="video in videos">
                <VideoPreview class="video" :video="video" :isPlaying="playerVideo ? video.id == playerVideo.id : false" />
            </li>
        </ul>
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
        playerVideo: Object,
        isLoadedByRequest: Boolean
    },
    mounted() {
        if (this.isLoadedByRequest) {
            this.$refs.videoYearGallery.getElementsByClassName('videoItem')[0].firstElementChild.focus();
        }
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

        h3 {
            position: relative;
            color: $headingColor;
            margin: 10px 0;
            text-align: center;
        }
    }
    .videoContent {
        display: grid;
        grid-template-columns: repeat( auto-fill, minmax(calc(120px + 6vw), 1fr) );
        padding: 0 20px;

        .videoItem {
            list-style: none;

            .video { width: 100%; }
        }
    }
</style>