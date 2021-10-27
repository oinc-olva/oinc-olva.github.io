<template>
    <div class="heroChannel">
        
    </div>
</template>

<script>
export default {
    name: 'HeroChannel',
    props: {
        channelName: null
    }
}
</script>

<style lang="scss" scoped>
    .heroChannel {
        height: 100%;
        background: linear-gradient(rgba(0, 0, 0, .6), rgba(0, 0, 0, .6)), url('/banner.jpg');
        background-size: 110%;
        background-position: center center;

        .container {
            display: flex;
            height: 100%;
            align-items: center;
        }
    }
    
</style>