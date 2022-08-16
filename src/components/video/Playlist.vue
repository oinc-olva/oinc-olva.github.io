<template>
    <div id="playlist" v-if="playlist" aria-label="Afspeellijst">
        <div id="playlistHeader">
            <h3>{{playlist.title}}</h3>
            <div id="playlistControls">
                <ul :aria-label="`Opties voor afspeellijst '${playlist.title}'`">
                    <li>
                        <button id="playlistLoop" :class="['icon', { active: this.playerPlaylistInfo.isLoop }]" @click="$emit('toggleLoop')" :title="`Herhalen (${this.playerPlaylistInfo.isLoop ? 'actief' : 'inactief'})`"><fa icon="repeat" /></button>
                    </li>
                    <li>
                        <button id="playlistShuffle" :class="['icon', { active: this.playerPlaylistInfo.isShuffle }]" @click="$emit('toggleShuffle')" :title="`Shuffle (${this.playerPlaylistInfo.isShuffle ? 'actief' : 'inactief'})`"><fa icon="shuffle" /></button>
                    </li>
                </ul>
            </div>
        </div>
        <div id="playlistBody">
            <ul id="playlistVideos" :aria-label="`Afspeellijst '${playlist.title}'`">
                <li v-for="videoId in playlist.videoIds.filter(videoId => this.videos.values.hasOwnProperty(videoId))" :key="videoId" :class="{ playing: videoId == this.$route.params.videoId }">
                    <router-link :to="{ name: 'Video', path: '/videos/:videoId/:videoName', params: { videoId: videoId, videoName: videos.values[videoId].videoPath }, query: { lijst: playerPlaylistInfo.playlistId } }" :aria-labelledby="`playlistVideoTitle-${videoId}`">
                        <div class="thumb">
                            <img :src="videos.values[videoId].thumb" :alt="videos.values[videoId].title">
                            <fa icon="play" />
                        </div>
                        <h4 :id="`playlistVideoTitle-${videoId}`" class="title">{{videos.values[videoId].title}}</h4>
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Playlist',
    props: {
        playlist: Object,
        videos: Object,
        playerPlaylistInfo: Object
    },
    mounted() {
        this.$emit('setPlaylistId', this.$route.query.lijst ?? '');
    }
}
</script>

<style lang="scss" scoped>
    #playlist {
        background: $sectionBackgroundDarker;
        border: 1px solid $sectionBorderColor;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    #playlistHeader {
        display: flex;
        align-items: center;
        margin: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid $sectionBorderColor;

        h3 {
            display: inline-block;
            flex: 1;
            color: $headingColor;
            font-size: .9em;
        }
        #playlistControls {
            display: inline-block;

            ul {
                list-style: none;

                li {
                    display: inline-block;

                    button {
                        color: gray;
                        font-size: .9em;
                        margin-left: 10px;
                        &.active { color: $accentColor; }
                    }
                }
            }
        }
    }
    #playlistBody {
        max-height: 500px;
        overflow: auto;

        #playlistVideos {
            list-style: none;

            li {
                &:hover, &:focus-within {
                    background-color: rgba(255, 255, 255, .01);
                    a { outline-offset: -2px; }
                }
                &.playing {
                    background-color: rgba(255, 255, 255, .05);
                    .thumb {
                        img { filter: brightness(.4); }
                        svg { display: block; }
                    }
                }

                a {
                    display: flex;
                    align-items: center;
                    padding: 20px;

                    .thumb {
                        position: relative;
                        margin-right: 20px;
                        height: 40px;
    
                        img {
                            height: 100%;
                            border-radius: 4px;
                        }
                        svg {
                            display: none;
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translateX(-50%) translateY(-50%);
                            color: white;
                        }
                    }
                    .title {
                        color: $headingColor;
                        font-weight: normal;
                        font-size: .8em;
                    }
                }
            }
        }
    }
</style>