<template>
    <transition name="fade">
        <div class="heroGeneral" :key="$route.name" :style="`background: linear-gradient(rgba(0, 0, 0, .3), rgba(0, 0, 0, .3)), ${$route.meta.heroBackground}`">
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
        background-size: 110% !important;
        background-position: center center !important;

        .pageTitle {
            color: white;
            font-size: 5.5em;
            text-shadow: 0px 0px 16px rgba(0, 0, 0,  .4);
        }
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
    
</style>