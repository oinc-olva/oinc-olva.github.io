<template>
    <transition name="fade">
        <div class="heroGeneral" :key="$route.name">
            <img class="background" :src="$route.meta.heroBackground" alt="Hero Background">
            <h1 class="pageTitle">{{$route.name}}</h1>
        </div>
    </transition>
</template>

<script>
export default {
    name: 'HeroGeneral'
}
</script>

<style lang="scss" scoped>
    .heroGeneral {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    .background {
        position: absolute;
        width: 100%;
        height: 100%;
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
    
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
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