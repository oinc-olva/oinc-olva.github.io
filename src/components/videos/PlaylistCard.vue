<template>
    <router-link class="playlistCard" :to="{ name: 'Video', path: '/videos/:videoId/:videoName', params: { videoId: firstVideoData.id, videoName: firstVideoData.videoPath }, query: { lijst: playlist.id } }" :aria-label="playlist.title" :aria-description="playlist.description">
        <div class="playlistCardMeta">
            <fa icon="play" />
            <span class="playlistCardVideoCount">{{playlist.videoIds.length}} video's</span>
        </div>
        <div class="playlistCardForeground">
            <div class="playlistCardForegroundInnerWrapper">
                <h3 id="playlistCardTitle">{{playlist.title}}</h3>
                <p ref="playlistCardDescription">{{playlist.description}}</p>
            </div>
        </div>
        <div class="playlistCardBackground" :style="{ background: `url('${firstVideoData.thumb}')` }"></div>
    </router-link>
</template>

<script>
export default {
    name: 'PlaylistCard',
    props: {
        playlist: Object,
        videos: Object
    },
    methods: {
        setDescriptionHeight() {
            const $description = this.$refs.playlistCardDescription;
            if ($description) $description.parentElement.setAttribute('style', `--descriptionHeight: ${$description.clientHeight}px`);
        }
    },
    computed: {
        firstVideoData() {
            return this.videos.values[this.playlist.videoIds[0]];
        }
    },
    mounted() {
        window.addEventListener('resize', this.setDescriptionHeight);
        this.$nextTick(() => this.setDescriptionHeight());
    },
    unmounted() {
        window.removeEventListener('resize', this.setDescriptionHeight);
    }
}
</script>

<style lang="scss" scoped>
    .playlistCard {
        display: inline-block;
        position: relative;
        box-sizing: border-box;
        width: 100%;
        height: 100%;
        border: 1px solid rgba(0, 0, 0, .2);
        border-radius: 10px;
        overflow: hidden;
        transition: border-color .4s ease-in-out;

        .playlistCardMeta {
            position: absolute;
            top: 30px;
            left: 30px;
            background-color: rgba(0, 0, 0, .6);
            color: rgb(228, 228, 228);
            font-size: .8em;
            padding: 5px 10px;
            border-radius: 5px;
            opacity: 0;
            z-index: 3;
            transition: opacity .2s ease-in-out;

            .playlistCardVideoCount { margin-left: 12px; }
        }
        .playlistCardForeground {
            position: absolute;
            bottom: 0;
            height: 8em;
            width: 100%;
            padding: 30px;
            box-sizing: border-box;
            background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, .6));
            pointer-events: none;
            z-index: 2;
            transition: height .4s ease-in-out;

            .playlistCardForegroundInnerWrapper {
                position: absolute;
                bottom: 20px;
                width: 100%;
                transform: translateY(var(--descriptionHeight));
                transition: transform .3s ease-in-out;

                h3 {
                    font-size: 90%;
                    font-weight: normal;
                    color: rgb(228, 228, 228);
                    transition: color .2s ease-in-out;
                }
                p {
                    width: calc(100% - 60px);
                    font-size: .8em;
                    margin-top: 5px;
                    white-space: initial;
                    opacity: 0;
                    color: lightgray;
                    transition: opacity .4s ease-in-out;
                }
            }
        }
        .playlistCardBackground {
            height: 100%;
            filter: brightness(.7);
            background: rgba(120, 120, 120, .1);
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-size: cover !important;
            transition: transform .4s ease-in-out;
        }

        &:hover, &:focus {
            border-color: $accentColor;

            .playlistCardMeta { opacity: 1; }
            .playlistCardForeground {
                height: 100%;

                .playlistCardForegroundInnerWrapper { transform: none; }
                h3 { color: $accentColor; }
                p { opacity: 1; }
            }
            .playlistCardBackground {
                transform: scale(1.1);
            }
        }
    }
</style>