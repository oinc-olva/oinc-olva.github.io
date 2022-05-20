<template>
    <div id="ipmContent">
        <div id="ipmMedia">
            <img v-if="post.media_type == 'IMAGE'" :src="post.media_url" :alt="post.caption">
            <InstagramVideo v-else-if="post.media_type == 'VIDEO'" :media="post.media_url" :thumb="post.thumb" :alt="post.caption" />
            <InstagramCarousel v-else :mediaList="post.children" :caption="post.caption" />
        </div>
        <div id="ipmMeta">
        </div>
    </div>
</template>

<script>
import InstagramVideo from './InstagramVideo.vue'
import InstagramCarousel from './InstagramCarousel.vue'

export default {
    name: 'InstagramPostModalContent',
    components: {
        InstagramVideo,
        InstagramCarousel
    },
    props: {
        post: Object,
        instagramName: String
    }
}
</script>

<style lang="scss" scoped>
    #ipmContent {
        display: flex;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
        width: 75vw;
        height: 45vw;
        max-width: 150vh;
        max-height: 90vh;
        background-color: $sectionBackgroundDark;
        border-radius: 4px;
        z-index: 3;

        &.modalContentSlideLeft-enter-from,
        &.modalContentSlideRight-leave-active {
            transform: translateX(-47%) translateY(-50%);
            opacity: 0;
        }
        &.modalContentSlideLeft-leave-active,
        &.modalContentSlideRight-enter-from {
            transform: translateX(-53%) translateY(-50%);
            opacity: 0;
        }
        &.modalContentSlideLeft-enter-active,
        &.modalContentSlideLeft-leave-active,
        &.modalContentSlideRight-enter-active,
        &.modalContentSlideRight-leave-active {
            transition: transform .35s ease-in-out,
                        opacity .2s ease-in-out;
        }
    }
    #ipmMedia {
        position: relative;
        aspect-ratio: 1 / 1;
        height: 100%;
        overflow: hidden;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }
    #ipmMeta {
        background-color: $sectionBackgroundLight
    }
</style>