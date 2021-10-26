<template>
    <div class="heroChannel" v-if="bannerImg" :style="{'background-image': ` linear-gradient(rgba(0, 0, 0, .7), rgba(0, 0, 0, .7)), url('${bannerImg}=w1707')`}">

    </div>
</template>

<script>
export default {
    name: 'HeroChannel',
    props: {
        bannerImg: String
    }
}
</script>

<style lang="scss" scoped>
    .heroChannel {
        height: 100%;
        background-size: 110%;
        background-position: center center;
    }
</style>