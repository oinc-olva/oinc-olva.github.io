<template>
    <div class="shareLightBox" @click.self="$emit('close')">
        <div class="content">
            <h3>Deel deze video:</h3>
            <button class="close icon" @click.stop="$emit('close')"><fa icon="times" /></button>
            <div class="shareLink" @click="select(this.$refs.sharePath)">
                <span ref="sharePath">{{path}}</span>
                <button class="icon" @click.stop="copy(this.$refs.sharePath)">Kopieer</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ShareLightBox',
    data() {
        return {
            path: null
        }
    },
    props: {
        videoId: String,
    },
    mounted() {
        this.path = `${window.location.host}/v/${this.videoId}`;
    },
    emits: [
        'close'
    ],
    methods: {
        select($el) {
            if (document.body.createTextRange) {
                const range = document.body.createTextRange();
                range.moveToElementText($el);
                range.select();
            } else if (window.getSelection) {
                const selection = window.getSelection();
                const range = document.createRange();
                range.selectNodeContents($el);
                selection.removeAllRanges();
                selection.addRange(range);
            } else {
                console.warn("Could not select text in node: Unsupported browser.");
            }
        },
        copy($el) {
            this.select($el);
            navigator.clipboard.writeText($el.innerText);
        }
    }
}
</script>

<style lang="scss" scoped>
    .shareLightBox {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: rgba(0, 0, 0, .7);
        z-index: 40;
    }
    .content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translateX(-50%) translateY(-50%);
        background-color: #3e424e;
        width: 400px;
        padding: 20px;
    }
    h3 {
        color: rgb(153, 152, 218);
        margin-bottom: 20px;
    }
    .icon {
        position: absolute;
        right: 20px;
        top: 20px;
    }
    .shareLink {
        position: relative;
        display: block;
        box-sizing: border-box;
        border: 1px solid gray;
        background-color: rgba(0, 0, 0, .2);
        color: rgb(204, 204, 204);
        font-size: .8em;
        border-radius: 4px;
        padding: 6px 12px;
        width: 100%;

        button {
            font-size: .9em;
            top: 50%;
            transform: translateY(-50%);
            text-transform: uppercase;
            font-weight: bold;
            color: gray;
        }
    }
</style>