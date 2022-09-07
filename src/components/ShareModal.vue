<template>
    <div id="shareModal" @click.self="$emit('close')" role="dialog" aria-labelledby="smTitle" aria-modal="true">
        <div id="smContent">
            <h3 id="smTitle">Delen</h3>
            <button id="smCloseBtn" class="icon" ref="firstTab" @click.stop="$emit('close')" aria-label="Deelvenster sluiten"><fa icon="times" /></button>
            <label id="smLinkLabel" for="smPath">Via URL:</label>
            <div id="smShareLink" @click="selectSmLink" role="none">
                <input id="smPath" ref="smPath" :value="url" readonly aria-label="URL naar video">
                <button id="smCopy" class="icon" ref="lastTab" @click.stop="copySmLink" aria-label="URL naar video kopiëren">Kopieer</button>
            </div>
        </div>
    </div>
</template>

<script>
import useModal from '../composables/modal.js';

export default {
    name: 'ShareModal',
    emits: [
        'close'
    ],
    props: {
        url: String,
    },
    methods: {
        selectSmLink() {
            if (this.$refs.smPath.select) {
                this.$refs.smPath.select();
            } else {
                this.$refs.smPath.setSelectionRange(0, this.$refs.smPath.value.length);
            }
        },
        copySmLink() {
            navigator.clipboard.writeText(this.$refs.smPath.value);
        }
    },
    setup() {
        useModal();
    }
}
</script>

<style lang="scss" scoped>
    #shareModal {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: rgba(0, 0, 0, .8);
        z-index: 40;
    }
    #smContent {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
        background-color: #3e424e;
        width: 600px;
        padding: 20px;
    }
    h3 {
        color: $headingColorBright;
        margin-bottom: 10px;
    }
    .icon {
        position: absolute;
        right: 20px;
        top: 20px;
    }
    #smLinkLabel {
        display: block;
        margin-left: 10px;
        margin-bottom: 10px;
        color: $textColorGray;
        z-index: 1;
    }
    #smShareLink {
        position: relative;
        display: block;
        box-sizing: border-box;
        padding: 6px 12px;
        width: 100%;
        background-color: rgba(0, 0, 0, .2);
        border: 1px solid $textColorGray;
        border-radius: 4px;
        font-size: .8em;
    }
    #smPath {
        background: transparent;
        color: $textColorGray;
        border: none;
        &:active, &:focus { outline: none; }
    }
    #smCopy {
        font-size: .9em;
        top: 50%;
        transform: translateY(-50%);
        color: $textColorGray;
        text-transform: uppercase;
        font-weight: bold;
    }
</style>