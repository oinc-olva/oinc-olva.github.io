<template>
    <section id="videoUploads" v-if="schoolYears" aria-labelledby="videoUploadsTitle">
        <div class="container">
            <h2 id="videoUploadsTitle">Laatste video's</h2>
            <VideoGallery :key="schoolYear" v-for="schoolYear in schoolYears.order.slice(0, shownYears)" class="gallery" :title="schoolYear" :videoIds="schoolYears.values[schoolYear]" :videos="videos" :playerVideo="playerVideo" :isLoadedByRequest="isGalleryLoadedByRequest" />
            <button id="videoUploadsShowMore" class="btn" @click="showMoreYears()" v-if="shownYears < schoolYears.order.length">Meer laden</button>
        </div>
    </section>
</template>

<script>
import VideoGallery from './VideoGallery.vue'

export default {
    name: 'VideoUploads',
    components: {
        VideoGallery
    },
    props: {
        videos: Object,
        schoolYears: Object,
        playerVideo: Object
    },
    data() {
        return {
            shownYears: 3,
            isGalleryLoadedByRequest: false
        }
    },
    methods: {
        showMoreYears() { this.shownYears++; this.isGalleryLoadedByRequest = true; }
    }
}
</script>

<style lang="scss" scoped>
    #videoUploads {
        background-color: #21242e;
        padding-top: 100px;
        padding-bottom: 100px;
    }
    #videoUploadsTitle {
        font-size: 2.5em;
        color: $headingColorBright;
    }
    #videoUploadsShowMore {
        display: block;
        margin: auto;
        margin-top: 80px;
    }
    .gallery {
        margin: 40px 0;
    }
    
    @media screen and (max-width: 600px) {
        #videoUploads {
            padding-top: 50px;
        }
        #videoUploadsTitle {
            text-align: center;
            font-size: 2em;
        }
    }
</style>