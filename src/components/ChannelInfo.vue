<template>
    <section id="channelInfo" aria-label="Korte info over het kanaal">
        <div class="container">
            <img id="channelThumb" src="/logo.jpg" alt="Logo kanaal">
            <div id="channelNameAndUrl">
                <span id="channelName">{{channelName}}</span>
                <div id="channelUrl">
                    🔗 <a class="link" :href="`https://youtube.com/${channelName}`" target="_blank" :aria-label="`Link naar ons kanaal (${channelName})`">https://youtube.com/{{channelName}}</a>
                </div>
            </div>
            <button id="subButton" class="btn" @click="subscribe" aria-label="Abonneren">Abonneren <span id="subCount">{{channelSubsFormatted}}</span></button>
        </div>
    </section>
</template>

<script>
export default {
    name: 'ChannelInfo',
    props: {
        channelName: String,
        channelSubsFormatted: String
    },
    methods: {
        subscribe() {
            window.open(`https://youtube.com/${this.channelName}?sub_confirmation=1`);
        }
    }
}
</script>

<style lang="scss" scoped>
    #channelInfo {
        background-color: #2c3141;
        color: $linkColor;
        padding: 40px 0;

        .container {
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }

    #channelThumb {
        display: inline-block;
        height: 6em;
        border-radius: 50%;
        box-shadow: 0px 0px 20px 4px rgba(0, 0, 0, .4);
        opacity: .6;
        margin-right: 40px;
    }

    #channelNameAndUrl {
        display: inline-block;
        flex: 1;
    }
    #channelName {
        color: $headingColorBright;
        font-size: 1.8em;
        line-height: 1.8em;
        margin-bottom: 5px;
        font-weight: bold;
        text-transform: lowercase;
    }
    #channelUrl {
        font-size: .75em;
        a { margin-left: 5px; }
    }

    #subButton {
        background-color: #ad3339;
        &:hover, &:active, &:focus { background-color: #a13339; }
    }
    #subCount {
        color: rgb(236, 212, 212);
        margin-left: 10px;
    }

    @media screen and (max-width: 820px) {
        .container {
            flex-direction: column;
        }
        #channelThumb {
            margin-right: 0;
            margin-bottom: 20px;
            height: 4em;
        }
        #channelNameAndUrl {
            #channelName, #channelUrl {
                display: block;
                text-align: center;
            }
            #channelName {
                text-align: center;
                margin-bottom: 0;
            }
        }
        #subButton {
            margin-top: 40px;
        }
    }
</style>