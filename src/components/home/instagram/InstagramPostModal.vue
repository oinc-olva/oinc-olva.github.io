<template>
    <div id="instagramPostModal" @click.self="$emit('close')" role="dialog" aria-label="Instagram post" aria-modal="true">
        <transition name="fade">
            <ShareModal v-if="isShareModalOpen" :url="getShareURL()" @close="() => { this.isShareModalOpen = false; setInputDisable(false); }" />
        </transition>
        <button id="ipmCloseBtn" class="icon" ref="firstTab" @click.stop="$emit('close')" title="Dialoogvenster sluiten"><fa icon="times" /></button>
        <button id="ipmPrevBtn" class="icon" @click.stop="prevPost" title="Vorige post">
            <img src="../../../assets/arrow.svg" alt="pijl naar links">
        </button>
        <transition :name="isContentSlideLeft ? 'modalContentSlideLeft' : 'modalContentSlideRight'">
            <InstagramPostModalContent :key="post" :post="post" :instagramName="instagramName" @share="() => { this.isShareModalOpen = true; setInputDisable(true); }" />
        </transition>
        <button id="ipmNextBtn" class="icon" ref="lastTab" @click.stop="nextPost" title="Volgende post">
            <img src="../../../assets/arrow.svg" alt="pijl naar rechts">
        </button>
    </div>
</template>

<script>
import useModal from '../../../composables/modal.js'

import InstagramPostModalContent from './InstagramPostModalContent.vue'
import ShareModal from '../../ShareModal.vue'

export default {
    name: 'InstagramPostModal',
    components: {
        InstagramPostModalContent,
        ShareModal
    },
    emits: [
        'close',
        'gotoPrev',
        'gotoNext'
    ],
    props: {
        post: Object,
        instagramName: String
    },
    data() {
        return {
            isContentSlideLeft: false,
            isShareModalOpen: false
        }
    },
    methods: {
        prevPost() {
            this.$emit('gotoPrev');
            this.isContentSlideLeft = false;
        },
        nextPost() {
            this.$emit('gotoNext');
            this.isContentSlideLeft = true;
        },
        getShareURL() {
            return window.location.href;
        }
    },
    setup() {
        const { setInputDisable } = useModal();
        return { setInputDisable };
    },
    beforeMount() {
        document.body.style.touchAction = 'none';
    },
    beforeUnmount() {
        document.body.style.touchAction = 'auto';
    }
}
</script>

<style lang="scss" scoped>
    #instagramPostModal {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 40;

        &.modalFade-enter-from,
        &.modalFade-leave-to {
            opacity: 0;
        }
        &.modalFade-enter-active,
        &.modalFade-leave-active {
            transition: opacity .2s ease-in-out;
        }
    }
    #ipmCloseBtn {
        position: absolute;
        right: 50px;
        top: 50px;
        width: 40px;
        height: 40px;
        line-height: 1em;
        font-size: 2em;
    }
    #ipmPrevBtn, #ipmNextBtn {
        position: absolute;
        top: 50%;
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 40px;
        height: 40px;
        border-radius: 50%;

        &:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }
    }
    #ipmPrevBtn {
        left: 50px;
    }
    #ipmNextBtn {
        right: 50px;
        img { transform: rotate(180deg); }
    }
    #shareModal {
        &.fade-enter-from {
            opacity: 0;
        }
        &.fade-enter-active, &.fade-leave-active {
            transition: opacity .2s ease-in-out;
        }
    }

    @media screen and (max-width: 1000px) {
        #ipmPrevBtn { left: 30px; }
        #ipmNextBtn, #ipmCloseBtn { right: 30px; }
    }
    @media screen and (max-width: 530px) {
        #ipmPrevBtn { left: 15px; }
        #ipmNextBtn, #ipmCloseBtn { right: 15px; }
    }
    @media screen and (max-width: 450px) {
        #ipmPrevBtn, #ipmNextBtn, #ipmCloseBtn {
            bottom: 20px;
            top: unset;
        }
        #ipmPrevBtn { left: calc(50vw - 100px); }
        #ipmNextBtn { right: calc(50vw - 100px); }
        #ipmCloseBtn {
            right: calc(50%);
            transform: translateX(50%);
        }
    }
</style>