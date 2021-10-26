<template>
    <section class="hero" :style="{'height': this.page == 'Home' ? '100vh' : '300px'}">
        <transition name="fade" mode="in-out">
            <HeroHome v-if="page == 'Home'" :videos="latestVideos" />
            <HeroChannel v-else-if="page == 'Videos'" :bannerImg="channelBanner" />
        </transition>
    </section>
</template>

<script>
import HeroHome from './HeroHome.vue'
import HeroChannel from './HeroChannel.vue'

export default {
    name: 'Hero',
    components: {
        HeroHome,
        HeroChannel
    },
    data() {
        return {
            videos: [],
            latestVideos: [],
            channelBanner: null
        }
    },
    computed: {
        page() { return this.$route.name }
    },
    async created() {
        let channelData = await this.fetchChannelData()
        this.videos = channelData.uploads.content
        this.latestVideos = this.videos.slice(0, 5)
        this.channelBanner = channelData.banner
    },
    methods: {
        async fetchChannelData() {
            const res = await fetch('channeldata.json')
            const data = await res.json()
            return data
        },
    }
}
</script>

<style lang="scss" scoped>
    .hero {
        position: relative;
        min-height: 500px;
        height: 500px;
        background-color: black;
        animation: fade 1s;
            @keyframes fade {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        transition: height .8s ease-out;
        
        & > div {
            &.fade-leave-active {
                position: absolute;
                z-index: 3;
                width: 100%;
                opacity: 0;
                transition: opacity .3s ease-in-out;
            }
            &.fade-enter-active {
                opacity: 0;
            }
        }
    }
</style>