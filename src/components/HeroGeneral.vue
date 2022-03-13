<template>
    <div id="heroGeneralWrapper" aria-label="Strook met titel">
        <div id="heroGeneral" :style="`top: ${this.scrollOffset}px`">
            <transition name="fade">
                <div class="heroGeneralInstance" :key="$route.name">
                    <img class="background" :src="$route.meta.heroBackground" alt="Achtergrond van strook met titel">
                    <h1 class="pageTitle">{{$route.name}}</h1>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HeroGeneral',
    data() {
        return {
            scrollOffset: 0
        }
    },
    methods: {
        scroll() {
            if (window.scrollY < 400) this.scrollOffset = -window.scrollY / 3;
        }
    },
    mounted() {
        document.addEventListener('scroll', this.scroll, false);
    },
    unmounted() {
        document.removeEventListener('scroll', this.scroll, false);
    }
}
</script>

<style lang="scss" scoped>
    #heroGeneralWrapper {
        height: 100%;

        &.fade-enter-active #heroGeneral {
            position: static;
            height: 100%;
        }
    }
    #heroGeneral {
        position: fixed;
        width: 100%;
        height: var(--heroHeight);
        transition: height .7s $pageTransitionFunction;
    }
    .heroGeneralInstance {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    .background {
        position: absolute;
        width: 100%;
        height: 110%;
        object-fit: cover;
        filter: brightness(.5);
    }
    .pageTitle {
        color: white;
        font-size: 5em;
        text-shadow: 0px 0px 16px rgba(0, 0, 0, 0.4);
        text-align: center;
        margin: 0 20px;
        z-index: 1;
        transition: font-size .3s ease-in-out;
    }
    
    .fade-leave-active {
        transition: opacity .4s $pageTransitionFunction;
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
        z-index: 1;
    }
    
    @media screen and (max-width: 600px) {
        .pageTitle {
            font-size: 3.5em;
        }
    }
    @media screen and (max-width: 380px) {
        .pageTitle {
            font-size: 2.5em;
        }
    }
</style>