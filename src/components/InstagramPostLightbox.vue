<template>
    <div id="instagramPostLightbox" @click.self="$emit('close')" aria-label="Instagram post venster" aria-role="none">
        <button id="iplCloseBtn" class="icon" @click.stop="$emit('close')" aria-label="Venster sluiten"><fa icon="times" /></button>
        <div id="iplContent">
            <div id="iplInstagramEmbed">
                <iframe :src="iframeLink" frameborder="0" :width="iframeHeight() / 2" :height="iframeHeight()"></iframe>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'InstagramPostLightbox',
    data() {
        return {
            embedScript: null
        }
    },
    computed: {
        iframeLink() {
            return `${this.post.permalink}embed/captioned/`;
        }
    },
    methods: {
        iframeHeight() {
            return window.innerHeight - 200;
        }
    },
    props: {
        post: Object
    },
    emits: [ 'close' ]
}
</script>

<style lang="scss" scoped>
    #instagramPostLightbox {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: rgba(0, 0, 0, .6);
        z-index: 40;
    }
    #iplContent {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
        padding: 20px;
    }
    #iplInstagramEmbed {
        position: relative;
        height: 100%;
        box-sizing: border-box;

        iframe {
            overflow: scroll;
        }
    }

    #iplCloseBtn {
        position: absolute;
        right: 100px;
        top: 80px;
        font-size: 2em;
    }
</style>