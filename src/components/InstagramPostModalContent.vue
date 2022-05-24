<template>
    <div id="ipmContent">
        <div id="ipmMedia">
            <img v-if="post.media_type == 'IMAGE'" :src="post.media_url" :alt="post.caption">
            <InstagramVideo v-else-if="post.media_type == 'VIDEO'" :media="post.media_url" :thumb="post.thumb" :alt="post.caption" />
            <InstagramCarousel v-else :mediaList="post.children" :caption="post.caption" />
        </div>
        <div id="ipmMeta">
            <a id="ipmAccountInfo" :href="`https://instagram.com/${instagramName}`" target="_blank">
                <img id="ipmAccountPhoto" src="/generated/img/web/logo_youtube.jpg" :alt="`Logo @${instagramName}`">
                <div id="ipmAccountMeta">
                    <span id="ipmAccountUsername">{{instagramName}}</span>
                    <div id="ipmAccountDetail">
                        <span id="ipmAccountLocation">OLVA / Onze Lieve Vrouwecollege Assebroek</span>
                        <span id="ipmAccountOpenLink">Klik om naar Instagram te gaan...</span>
                    </div>
                </div>
                <fa id="ipmAccountLinkIcon" icon="external-link-alt" />
            </a>
            <p id="ipmCaption" v-if="post.caption">{{post.caption}}</p>
            <div id="ipmBottomInfo">
                <span id="ipmDate">&#169; Gepubliceerd op {{post.date}}</span>
                <div id="ipmMetaButtons">
                    <button id="ipmShare" class="icon" title="Post delen" aria-label="Post delen"><fa icon="share-alt" /></button>
                    <a id="ipmOpenLink" class="icon" :href="post.permalink" target="_blank" title="Open post op Instagram" aria-label="Open post op Instagram"><fa icon="external-link-alt" /></a>
                </div>
            </div>
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
        display: flex;
        flex-direction: column;
        flex: 1;
        background-color: $sectionBackgroundLight;
        padding: 20px;
    }
    #ipmAccountInfo {
        display: flex;
        align-items: center;
        background-color: rgba(0, 0, 0, .2);
        padding: 10px;
        border-radius: 10px;
        transition: background-color .2s ease-in-out;

        &:hover, &:focus {
            background-color: rgba(0, 0, 0, .3);

            #ipmAccountOpenLink, #ipmAccountLinkIcon { opacity: 1; }
            #ipmAccountLocation { opacity: 0; }
        }
    }
    #ipmAccountPhoto {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    #ipmAccountMeta {
        flex: 1;
        margin-left: 20px;
    }
    #ipmAccountUsername {
        display: block;
        color: $headingColorBright;
    }
    #ipmAccountDetail {
        position: relative;
        display: block;
        color: gray;
        font-size: .7em;
        line-height: 1.2em;
    }
    #ipmAccountOpenLink {
        position: absolute;
        left: 0;
        opacity: 0;
    }
    #ipmAccountLinkIcon {
        position: absolute;
        right: 20px;
        color: gray;
        opacity: 0;
    }
    #ipmAccountLocation, #ipmAccountOpenLink, #ipmAccountLinkIcon {
        transition: opacity .2s ease-in-out;
    }
    #ipmCaption {
        padding: 10px 30px;
        margin: 30px 20px 0 35px;
        white-space: pre-wrap;
        color: $textColorGray;
        border-left: 1px solid $textColorGray;
    }
    #ipmBottomInfo {
        display: flex;
        margin: auto 10px 5px;
    }
    #ipmDate {
        flex: 1;
        color: rgb(139, 139, 139)
    }
    #ipmMetaButtons {
        margin-left: 20px;

        button, a {
            font-size: 1.2em;
            color: white;
            margin: 0 10px;
        }
    }
</style>