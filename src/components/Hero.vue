<template>
    <section
        v-if="latestVideos"
        id="hero"
        :style="{'height': this.page == 'Home' ? '100vh' : (this.page == 'Video' ? '0' : '400px')}"
        :aria-label="page == 'Home' ? 'Slideshow van laatste video\'s' : (page != 'Video' ? 'Strook met titel van pagina' : 'Niet-zichtbare strook')">
        <transition name="fade" mode="in-out">
            <HeroHome v-if="page == 'Home'" :videos="latestVideos.slice(0, 4)" />
            <HeroGeneral v-else-if="page != 'Video'" />
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
    #hero {
        position: relative;
        height: 0;
        animation: fade 1s;
            @keyframes fade {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        transition: height 1s $pageTransitionFunction;
        
        & > div {
            &.fade-leave-active {
                position: absolute;
                z-index: 6;
                width: 100%;
                opacity: 0;
                transition: opacity .3s $pageTransitionFunction;
            }
            &.fade-enter-active {
                opacity: 0;
            }
        }
    }
</style>