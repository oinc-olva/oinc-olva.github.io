<template>
    <section
        v-if="latestVideos"
        id="hero"
        :style="{ '--heroHeight': heroHeight, 'z-index': this.page == 'Home' ? 0 : -1 }"
        :aria-label="page == 'Home' ? 'Slideshow van laatste video\'s' : (page != 'Video' ? 'Strook met titel van pagina' : 'Niet-zichtbare strook')">
        <transition name="fade" mode="in-out">
            <HeroHome v-if="page == 'Home'" :videos="latestVideos" />
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
        page() { return this.$route.name },
        heroHeight() {
            let heroHeight = this.$route.meta.heroHeight;
            if (heroHeight == 'vh') return '100vh';
            return heroHeight + 'px'
        }
    }    
}
</script>

<style lang="scss" scoped>
    #hero {
        position: relative;
        height: var(--heroHeight);
        animation: fade .6s;
            @keyframes fade {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        transition: height .8s $pageTransitionFunction;
        
        & > div {
            &.fade-leave-active {
                position: absolute;
                width: 100%;
                opacity: 0;
                transition: opacity .4s $pageTransitionFunction;
            }
            &.fade-enter-active {
                opacity: 0;
            }
        }
    }
</style>