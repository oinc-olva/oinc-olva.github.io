<template>
    <div id="shareLightBox" @click.self="$emit('close')" aria-label="Deelvenster" aria-role="none">
        <div id="slbContent">
            <h3>Delen</h3>
            <button id="slbCloseBtn" class="icon" @click.stop="$emit('close')" aria-label="Deelvenster sluiten"><fa icon="times" /></button>
            <label id="slbLinkLabel" for="slbPath">Via URL:</label>
            <div id="slbShareLink" @click="selectSlbLink" role="none">
                <input id="slbPath" ref="slbPath" :value="url" readonly aria-label="URL naar video">
                <button id="slbCopy" class="icon" @click.stop="copySlbLink" aria-label="URL naar video kopiëren">Kopieer</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ShareLightBox',
    props: {
        url: String,
    },
    emits: [
        'close'
    ],
    methods: {
        selectSlbLink() {
            if (this.$refs.slbPath.select) {
                this.$refs.slbPath.select();
            } else {
                this.$refs.slbPath.setSelectionRange(0, this.$refs.slbPath.value.length);
            }
        },
        copySlbLink() {
            navigator.clipboard.writeText(this.$refs.slbPath.value);
        }
    }
}
</script>

<style lang="scss" scoped>
    #shareLightBox {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: rgba(0, 0, 0, .8);
        z-index: 40;
    }
    #slbContent {
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
    #slbLinkLabel {
        display: block;
        margin-left: 10px;
        margin-bottom: 10px;
        color: $textColorGray;
        z-index: 1;
    }
    #slbShareLink {
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
    #slbPath {
        background: transparent;
        color: $textColorGray;
        border: none;
        &:active, &:focus { outline: none; }
    }
    #slbCopy {
        font-size: .9em;
        top: 50%;
        transform: translateY(-50%);
        color: $textColorGray;
        text-transform: uppercase;
        font-weight: bold;
    }
</style>