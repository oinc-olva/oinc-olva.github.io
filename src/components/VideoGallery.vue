<template>
    <section class="videoGallery" v-if="publishSchoolYears" aria-label="Videogalerij">
        <div class="container">
            <h2>Laatste video's</h2>
            <VideoYearGallery class="yearGallery" :key="schoolYear" v-for="schoolYear in publishSchoolYears.slice(0, shownYears)" :schoolYear="schoolYear" :videos="uploads[schoolYear]" :playerVideo="playerVideo" :isLoadedByRequest="isLoadMoreClicked" />
            <button class="showMore btn" @click="showMoreYears()" v-if="shownYears < publishSchoolYears.length">Meer laden</button>
        </div>
    </section>
</template>

<script>
import VideoYearGallery from './VideoYearGallery.vue'

export default {
    name: 'VideoGallery',
    components: {
        VideoYearGallery
    },
    props: {
        uploads: Object,
        publishSchoolYears: Array,
        playerVideo: Object
    },
    data() {
        return {
            shownYears: 3,
            isLoadMoreClicked: false
        }
    },
    methods: {
        showMoreYears() { this.shownYears++; this.isLoadMoreClicked = true; }
    }
}
</script>

<style lang="scss" scoped>
    .videoGallery {
        background-color: #21242e;
        padding-top: 100px;
        padding-bottom: 100px;

        h2 {
            font-size: 2.5em;
            color: $headingColorBright;
        }
    }
    .showMore {
        display: block;
        margin: auto;
        margin-top: 80px;
    }
    
    @media screen and (max-width: 600px) {
        .videoGallery {
            padding-top: 50px;
        }
        h2 {
            text-align: center;
            font-size: 2em;
        }
    }
</style>