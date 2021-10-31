<template>
    <section class="hero" v-if="page != 'Video'" :style="{'height': this.page == 'Home' ? '100vh' : '300px'}">
        <transition name="fade" mode="in-out">
            <HeroHome v-if="page == 'Home'" :videos="latestVideos.slice(0, 5)" />
            <HeroGeneral v-else />
        </transition>
    </section>
</template>

<script>
import HeroHome from './HeroHome.vue'
import HeroGeneral from './HeroGeneral.vue'

export default {
    name: 'Hero',
    components: {
        HeroHome,
        HeroGeneral
    },
    props: {
        latestVideos: Array
    },
    computed: {
        page() { return this.$route.name }
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
        transition: height .8s cubic-bezier(.2,.91,.24,.94);
        
        & > div {
            &.fade-leave-active {
                position: absolute;
                z-index: 3;
                width: 100%;
                opacity: 0;
                transition: opacity .15s ease-in-out;
            }
            &.fade-enter-active {
                opacity: 0;
            }
        }
    }
</style>