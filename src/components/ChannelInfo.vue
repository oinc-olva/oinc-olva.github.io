<template>
    <div class="channelInfo">
        <div class="container">
            <img class="thumb" src="/logo.jpg" alt="">
            <div class="info">
                <h2>{{channelName}}</h2>
                🔗 <a class="link" :href="`https://youtube.com/${channelName}`" target="_blank">https://youtube.com/{{channelName}}</a>
            </div>
            <button class="subButton btn" @click="subscribe">Abonneren <span class="subCount">{{channelSubsFormatted}}</span></button>
        </div>
    </div>
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

        .container {
            position: relative;
            display: flex;
            align-items: center;
            height: 200px;
        }
    }
    img {
        height: 50%;
        border-radius: 50%;
        box-shadow: 0px 0px 15px 5px rgba(0, 0, 0, .6);
        opacity: .6;
    }
    .info {
        padding: 5px 15px 5px 40px;
        h2 {
            color: rgb(130, 135, 179);
            font-size: 1.8em;
            text-transform: lowercase;
        }
        .link {
            color: gray;
            font-size: .8em;
            margin-left: 5px;
            &::before { background-color: gray; }
        }
    }
    .subButton {
        position: absolute;
        right: 0;
        background-color: #ee353e;
        &:hover { background-color: #e03039; }

        .subCount {
            color: lightgray;
            margin-left: 10px;
        }
    }
</style>