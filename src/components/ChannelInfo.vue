<template>
    <section class="channelInfo">
        <div class="container">
            <img class="thumb" src="/logo.jpg" alt="">
            <div class="nameAndUrl">
                <h2>{{channelName}}</h2>
                <div class="channelUrl">
                    🔗 <a class="link" :href="`https://youtube.com/${channelName}`" target="_blank">https://youtube.com/{{channelName}}</a>
                </div>
            </div>
            <button class="subButton btn" @click="subscribe">Abonneren <span class="subCount">{{channelSubsFormatted}}</span></button>
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
    .channelInfo {
        background-color: #2c3141;
        padding: 40px 0;

        .container {
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }
    img {
        display: inline-block;
        height: 6em;
        border-radius: 50%;
        box-shadow: 0px 0px 20px 4px rgba(0, 0, 0, .4);
        opacity: .6;
        margin-right: 40px;
    }
    .nameAndUrl {
        display: inline-block;
        flex: 1;

        h2 {
            color: rgb(133, 140, 204);
            font-size: 1.8em;
            margin-bottom: 5px;
            text-transform: lowercase;
        }
        .channelUrl {
            font-size: .75em;
            a {
                color: gray;
                margin-left: 5px;
                &::before { background-color: gray; }
            }
        }
    }
    .subButton {
        background-color: #ad3339;
        &:hover { background-color: #a13339; }

        .subCount {
            color: rgb(236, 212, 212);
            margin-left: 10px;
        }
    }

    @media screen and (max-width: 820px) {
        .container {
            flex-direction: column;
        }
        .thumb {
            margin-right: 0;
            margin-bottom: 20px;
            height: 4em;
        }
        .nameAndUrl {
            .channelUrl, h2 {
                text-align: center;
            }
            h2 {
                text-align: center;
                margin-bottom: 0;
            }
        }
        .subButton {
            margin-top: 40px;
        }
    }
</style>