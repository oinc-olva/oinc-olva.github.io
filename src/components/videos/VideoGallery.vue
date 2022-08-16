<template>
    <div class="videoGallery" ref="videoGallery">
        <h3>{{title}}</h3>
        <ul class="videoContent" :aria-label="title">
            <li class="videoItem" :key="videoId" v-for="videoId in videoIds.slice(0, shownVideoCount)">
                <VideoPreview class="videoPreview" :video="videos.values[videoId]" :isPlaying="playerVideo ? videos.values[videoId].id == playerVideo.id : false" />
            </li>
        </ul>
        <div class="galleryShowMore" v-if="shownVideoCount < videoIds.length">
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
        videos: Object,
        videoIds: Array,
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
            handler(newVal, oldVal) {
                this.$nextTick(() => {
                    if (newVal > oldVal) this.$refs.videoGallery.getElementsByClassName('videoItem')[oldVal].firstElementChild.focus();
                })
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    .videoGallery {
        background-color: $sectionBackgroundDarker;
        padding: 10px;
        border: 1px solid $sectionBorderColor;
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