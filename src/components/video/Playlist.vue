<template>
    <div id="playlist" v-if="playerPlaylist" aria-label="Afspeellijst">
        <div id="playlistHeader">
            <h3>{{playerPlaylist.title}}</h3>
            <div id="playlistControls">
                <ul :aria-label="`Opties voor afspeellijst '${playerPlaylist.title}'`">
                    <li>
                        <button id="playlistLoop" :class="['icon', { active: this.playerPlaylistInfo.isLoop }]" @click="toggleLoop" :title="`Herhalen (${this.playerPlaylistInfo.isLoop ? 'actief' : 'inactief'})`"><fa icon="repeat" /></button>
                    </li>
                    <li>
                        <button id="playlistShuffle" :class="['icon', { active: this.playerPlaylistInfo.isShuffle }]" @click="toggleShuffle" :title="`Shuffle (${this.playerPlaylistInfo.isShuffle ? 'actief' : 'inactief'})`"><fa icon="shuffle" /></button>
                    </li>
                </ul>
            </div>
        </div>
        <div id="playlistBody">
            <ul id="playlistVideos" :aria-label="`Afspeellijst '${playerPlaylist.title}'`">
                <li v-for="videoId in playerPlaylist.videoIds.filter(videoId => this.videos.values.hasOwnProperty(videoId))" :key="videoId" :class="{ playing: videoId == currentVideoId }">
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
        playlists: Array,
        videos: Object,
        currentVideoId: String,
        playerPlaylistInfo: Object
    },
    data() {
        return {
            playerPlaylist: null
        }
    },
    methods: {
        setPlaylistId(id) {
            this.playerPlaylistInfo.playlistId = id;

            if (id != '') {
                this.playerPlaylist = this.playlists.find(obj => obj.id == id);
                if (!this.playerPlaylist) {
                    this.$router.push({
                        name: 'Video',
                        path: `/videos/:videoId/:videoName`,
                        params: {
                            videoId: this.$route.params.videoId,
                            videoName: this.$route.params.videoName
                        }
                    });
                }
            } else {
                this.playerPlaylist = null;
            }
        },
        toggleLoop() {
            this.playerPlaylistInfo.isLoop = !this.playerPlaylistInfo.isLoop;
        },
        toggleShuffle() {
            this.playerPlaylistInfo.isShuffle = !this.playerPlaylistInfo.isShuffle;
        }
    },
    mounted() {
        this.setPlaylistId(this.$route.query.lijst ?? '');
    },
    watch: {
        $route(to) {
            if (to.name == 'Video' && this.playerPlaylistInfo.playlistId !== to.query.lijst) this.setPlaylistId(to.query.lijst ?? '');
        }
    }
}
</script>

<style lang="scss" scoped>
    #playlist {
        display: flex;
        flex-direction: column;
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
        flex: 1;
        max-height: 500px;
        overflow-x: hidden;
        overflow-y: auto;

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