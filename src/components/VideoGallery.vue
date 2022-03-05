<template>
    <div class="videoGallery" ref="videoGallery">
        <h3>{{title}}</h3>
        <ul class="videoContent" :aria-label="title">
            <li class="videoItem" :key="video" v-for="video in videos.slice(0, shownVideoCount)">
                <VideoPreview class="videoPreview" :video="video" :isPlaying="playerVideo ? video.id == playerVideo.id : false" />
            </li>
        </ul>
        <div class="galleryShowMore" v-if="shownVideoCount < videos.length">
            <button class="btn" @click="$emit('increaseShownVideoCount')">Meer laden</button>
        </div>
    </div>
</template>

<script>
import VideoPreview from './VideoPreview.vue'

export default {
    name: 'VideoGallery',
    components: {
        VideoPreview
    },
    props: {
        title: String,
        videos: Array,
        playerVideo: Object,
        shownVideoCount: Number,
        isLoadedByRequest: Boolean
    },
    emits: [ 'increaseShownVideoCount' ],
    mounted() {
        if (this.isLoadedByRequest) this.$refs.videoGallery.getElementsByClassName('videoItem')[0].firstElementChild.focus();
    },
    watch: {
        shownVideoCount: {
            handler(_, oldVal) {
                this.$nextTick(() => {
                    this.$refs.videoGallery.getElementsByClassName('videoItem')[oldVal].firstElementChild.focus();
                })
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    .videoGallery {
        background-color: rgba(0, 0, 0, .1);
        padding: 10px;
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
        grid-template-columns: repeat( auto-fill, minmax(calc(140px + 7%), 1fr) );
        padding: 0 calc(5px + 3%);

        .videoItem {
            list-style: none;

            .videoPreview { width: 100%; }
        }
    }
    .galleryShowMore {
        text-align: center;
        margin: 40px 0 20px;
    }
</style>