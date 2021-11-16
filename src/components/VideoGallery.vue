<template>
    <section class="videoGallery" v-if="publishSchoolYears">
        <div class="container">
            <h1>Laatste video's</h1>
            <VideoYearGallery :key="schoolYear" v-for="schoolYear in publishSchoolYears.slice(0, shownYears)" :schoolYear="schoolYear" :videos="uploads[schoolYear]" />
            <button class="showMore" @click="showMoreYears()" v-if="shownYears < publishSchoolYears.length">Meer laden</button>
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
        publishSchoolYears: Array
    },
    data() {
        return {
            shownYears: 3
        }
    },
    methods: {
        showMoreYears() { this.shownYears++; }
    }
}
</script>

<style lang="scss" scoped>
    .videoGallery {
        background-color: #21242e;
        padding-top: 100px;
        padding-bottom: 100px;

        h1 {
            font-size: 2.5em;
            color: rgb(94, 99, 136);
        }
    }
    .showMore {
        display: block;
        margin: auto;
        margin-top: 80px;
    }
</style>