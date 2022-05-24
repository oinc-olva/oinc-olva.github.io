<template>
    <div id="ipmContent" :class="{'draggingCarouselMouse': this.isDraggingCarouselMouse}">
        <div id="ipmMedia">
            <img v-if="post.media_type == 'IMAGE'" :src="post.media_url" :alt="post.caption">
            <InstagramVideo v-else-if="post.media_type == 'VIDEO'" :media="post.media_url" :thumb="post.thumb" :alt="post.caption" />
            <InstagramCarousel v-else :mediaList="post.children" :caption="post.caption" @startDragMouse="this.isDraggingCarouselMouse = true" @endDragMouse="this.isDraggingCarouselMouse = false" />
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
            <div id="ipmCaptionWrapper">
                <div id="ipmCaptionInnerWrapper">
                    <p id="ipmCaption" v-if="post.caption">{{post.caption}}</p>
                </div>
            </div>
            <div id="ipmBottomInfo">
                <span id="ipmDate">{{post.date}}</span>
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
    },
    data() {
        return {
            isDraggingCarouselMouse: false
        }
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
        width: 45vw;
        height: 45vw;
        max-width: 90vh;
        max-height: 90vh;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    #ipmMeta {
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        width: 30vw;
        background-color: $sectionBackgroundLight;
        padding: 20px;
    }
    #ipmAccountInfo {
        display: flex;
        align-items: center;
        background-color: $sectionBackgroundSemiLight;
        padding: 10px;
        border-radius: 10px;
        transition: background-color .2s ease-in-out;

        &:hover, &:focus {
            background-color: $sectionBackgroundDark;

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
        top: 50%;
        left: 0;
        transform: translateY(-50%);
        width: 70%;
        opacity: 0;
    }
    #ipmAccountLinkIcon {
        position: absolute;
        right: 20px;
        color: gray;
        padding: 10px;
        opacity: 0;
    }
    #ipmAccountLocation, #ipmAccountOpenLink, #ipmAccountLinkIcon {
        transition: opacity .2s ease-in-out;
    }
    #ipmCaptionWrapper {
        position: relative;
        flex: 1;
        margin: 30px 20px 20px 35px;
        overflow-x: hidden;
        overflow-y: auto;
    }
    #ipmCaption {
        white-space: pre-wrap;
        color: $textColorGray;
        padding: 10px 30px;
        border-left: 1px solid $textColorGray;
        max-height: 100%;
    }
    #ipmBottomInfo {
        display: flex;
        align-items: center;
        margin: 0 10px 5px;
    }
    #ipmDate {
        flex: 1;
        color: rgb(139, 139, 139);

        &::before {
            content: '© Gepubliceerd op ';
        }
    }
    #ipmMetaButtons {
        margin-left: 20px;

        button, a {
            font-size: 1.2em;
            color: white;
            margin: 0 10px;
        }
    }

    @media screen and (max-width: 1000px) {
        #ipmDate::before { content: '© '; }
    }
    @media screen and (max-width: 800px) {
        #ipmContent {
            flex-direction: column;
            width: 65vw;
            height: 90vh;
            max-width: 90vh;
            max-height: 150vh;
            overflow-y: auto;
            overflow-x: hidden;

            &.draggingCarouselMouse {
                overflow: visible;

                #ipmMeta {
                    overflow: hidden;
                }
                #ipmCaptionWrapper {
                    overflow: visible;
                }
            }
        }
        #ipmMedia {
            width: 65vw;
            height: 65vw;
            max-width: 130vw;
            max-height: 130vw;
        }
        #ipmMeta {
            width: 65vw;
            flex: 1;
        }
        #ipmCaptionWrapper {
            overflow-y: visible;
        }
    }
    @media screen and (max-width: 450px) {
        #ipmContent {
            width: 80vw;
            height: 80vh;
            top: calc(50% - 20px);
        }
        #ipmMedia {
            width: 80vw;
            height: 80vw;
        }
        #ipmMeta {
            width: 80vw;
        }
        #ipmCaptionWrapper {
            margin: 30px 10px 30px 20px
        }
    }
</style>