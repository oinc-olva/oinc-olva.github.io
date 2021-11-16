<template>
    <transition name="fade">
        <div class="heroGeneral" :key="$route.name">
            <div class="background" :style="`background: linear-gradient(rgba(0, 0, 0, .4), rgba(0, 0, 0, .4)), ${$route.meta.heroBackground}`"></div>
            <h1 class="pageTitle">{{$route.name}}</h1>
        </div>
    </transition>
</template>

<script>
export default {
    name: 'HeroGeneral',
    props: {
        heroBackground: String
    }
}
</script>

<style lang="scss" scoped>
    .heroGeneral {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;

        .background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-size: 100% !important;
            background-position: center center !important;
        }
        .pageTitle {
            color: white;
            font-size: 5.5em;
            text-shadow: 0px 0px 16px rgba(0, 0, 0, 0.4);
            z-index: 1;
        }
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
    
</style>