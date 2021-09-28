<template>
    <section class="videoslideshow">
        <ul>
            <li :key="video" v-for="video in videos">
                <img :src="video.thumbmaxres" alt="">
                <h2>{{video.title}}</h2>
            </li>
        </ul>
    </section>
</template>

<script>
export default {
    name: 'Videoslideshow',
    props: {
        videos: Array
    }
}
</script>

<style lang="scss" scoped>
    ul, li, img {
        width: 100%;
    }
</style>