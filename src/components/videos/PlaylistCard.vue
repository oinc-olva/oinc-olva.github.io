<template>
    <router-link class="playlistCard" :to="{ name: 'Video', path: '/videos/:videoId/:videoPath', params: { videoId: firstVideoData.id, videoPath: firstVideoData.videoPath }, query: { lijst: playlist.id } }" :aria-labelledby="`playlistCardTitle-${this.playlist.id}`" :aria-describedby="`playlistCardDescription-${this.playlist.id}`">
        <div class="playlistCardMeta">
            <fa icon="play" />
            <span class="playlistCardVideoCount">{{playlist.videoIds.length}} video's</span>
        </div>
        <div class="playlistCardForeground">
            <div class="playlistCardForegroundInnerWrapper">
                <h3 :id="`playlistCardTitle-${this.playlist.id}`" class="playlistCardTitle">{{playlist.title}}</h3>
                <p ref="playlistCardDescription" :id="`playlistCardDescription-${this.playlist.id}`">{{playlist.description}}</p>
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
    computed: {
        firstVideoData() {
            return this.videos.values[this.playlist.videoIds[0]];
        }
    }
}
</script>

<style lang="scss" scoped>
    $cardPadding: 30px;

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
            top: $cardPadding;
            left: $cardPadding;
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
            padding: $cardPadding;
            box-sizing: border-box;
            background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, .6));
            pointer-events: none;
            z-index: 2;
            transition: height .4s ease-in-out;

            .playlistCardForegroundInnerWrapper {
                position: absolute;
                display: flex;
                flex-direction: column;
                bottom: $cardPadding;
                transform: translateY(100%);
                width: 100%;
                max-height: calc(100% - #{ $cardPadding * 3.5 });
                transition: transform .3s ease-in-out,
                            bottom .3s ease-in-out;

                h3 {
                    display: inline-block;
                    width: calc(100% - #{ $cardPadding * 2 });
                    font-size: 90%;
                    font-weight: normal;
                    color: rgb(228, 228, 228);
                    white-space: initial;
                    transform: translateY(-100%);
                    transition: transform .3s ease-in-out,
                                color .2s ease-in-out;
                }
                p {
                    display: inline-block;
                    flex: 1;
                    height: 0;
                    width: calc(100% - #{ $cardPadding * 2 });
                    font-size: .8em;
                    margin-top: 5px;
                    white-space: initial;
                    opacity: 0;
                    color: lightgray;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    transition: opacity .35s ease-in-out;
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
            transition: transform .4s ease-in-out,
                        filter .4s ease-in-out;
        }

        &:hover, &:focus {
            border-color: $accentColor;

            .playlistCardMeta { opacity: 1; }
            .playlistCardForeground {
                height: 100%;

                .playlistCardForegroundInnerWrapper {
                    bottom: $cardPadding;
                    transform: none;
                }
                h3 {
                    color: $accentColor;
                    transform: none;
                }
                p { opacity: 1; }
            }
            .playlistCardBackground {
                transform: scale(1.1);
                filter: brightness(.6);
            }
        }
    }
</style>