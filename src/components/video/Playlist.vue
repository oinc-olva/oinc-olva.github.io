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
                    <component :is="isOnVideoPage ? 'router-link' : 'button'" :to="isOnVideoPage ? { name: 'Video', path: '/videos/:videoId/:videoPath', params: { videoId: videoId, videoPath: videos.values[videoId].videoPath }, query: { lijst: playerPlaylistInfo.playlistId } } : null" :aria-labelledby="`playlistVideoTitle-${videoId}`"  @click="isOnVideoPage ? null : $emit('setCurrentVideoId', videoId)">
                        <div class="thumb">
                            <img :src="videos.values[videoId].thumb" :alt="videos.values[videoId].title">
                            <fa icon="play" class="playIcon" />
                        </div>
                        <h4 :id="`playlistVideoTitle-${videoId}`" class="title">{{videos.values[videoId].title}}</h4>
                    </component>
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
        playerPlaylistInfo: Object,
        isOnVideoPage: Boolean
    },
    emits: [ 'setCurrentVideoId' ],
    data() {
        return {
            playerPlaylist: null
        }
    },
    methods: {
        setPlaylistId(playlistid, currentVideoId) {
            this.playerPlaylistInfo.playlistId = playlistid; // Zet nieuwe afspeellijst-ID
            if (playlistid != '') { // Als er nu een afspeellijst actief is...
                this.playerPlaylist = this.playlists.find(obj => obj.id == playlistid); // Zoek de afspeellijst met de bijbehorende afspeellijst-ID

                if (this.playerPlaylist) { // Als de nieuwe afspeellijst bestaat...
                    this.refillNotWatchedVideoIds(currentVideoId); // Maak een lijst van de nog niet geziene video's in die afspeellijst
                    this.calculateNextVideoId(currentVideoId); // Kies een video om af te spelen na het eindigen van de huidige video
                } else { // Als de actieve afspeellijst niet bestaat, verander de URL
                    this.$router.push({
                        name: 'Video',
                        path: `/videos/:videoId/:videoPath`,
                        params: {
                            videoId: currentVideoId,
                            videoPath: this.videos.values[currentVideoId].videoPath
                        }
                    });
                }
            } else { // Als er nu geen afspeellijst meer actief is (het is dus gesloten)...
                this.playerPlaylist = null;
            }
        },
        toggleLoop() {
            this.playerPlaylistInfo.isLoop = !this.playerPlaylistInfo.isLoop;
            this.calculateNextVideoId(this.currentVideoId);
        },
        toggleShuffle() {
            this.playerPlaylistInfo.isShuffle = !this.playerPlaylistInfo.isShuffle;
            if (this.playerPlaylistInfo.isShuffle && this.playerPlaylistInfo.notWatchedVideoIds.length == 0) this.refillNotWatchedVideoIds(this.currentVideoId);
            this.calculateNextVideoId(this.currentVideoId);
        },
        refillNotWatchedVideoIds(currentVideoId) {
            this.playerPlaylistInfo.notWatchedVideoIds = this.playerPlaylist.videoIds.filter(videoId => videoId != currentVideoId);
        },
        calculateNextVideoId(currentVideoId) {
            if (this.playerPlaylistInfo.isShuffle) { // Als in shuffle-modus
                if (this.playerPlaylistInfo.notWatchedVideoIds.length == 0) { // Als er geen video's meer te bekijken zijn...
                    if (this.playerPlaylistInfo.isLoop) { // Als in loop-modus...
                        if (this.playerPlaylist.videoIds.length == 1) { // Als er maar één video is in de afspeellijst, herhaal die video
                            this.playerPlaylistInfo.nextVideoId = currentVideoId;
                            return;
                        } else { // Als er meerdere video's zijn in de afspeellijst, hervul de lijst van niet-bekeken video's
                            this.refillNotWatchedVideoIds(currentVideoId);
                        }
                    } else { // Als niet in loop-modus, alle video's zijn bekeken van de afspeellijst
                        this.playerPlaylistInfo.nextVideoId = '';
                        return;
                    }
                }

                // Neem een willekeurige video uit de lijst van niet-bekeken video's
                this.playerPlaylistInfo.nextVideoId = this.playerPlaylistInfo.notWatchedVideoIds[Math.floor(Math.random() * this.playerPlaylistInfo.notWatchedVideoIds.length)]
            
            } else { // Als niet in shuffle-modus
                if (this.playerPlaylist.videoIds[this.playerPlaylist.videoIds.length - 1] == currentVideoId) { // Als de laatste video van de afspeellijst op dit moment wordt bekeken...
                    if (this.playerPlaylistInfo.isLoop) { // Als in loop-modus, neem de eerste video
                        this.playerPlaylistInfo.nextVideoId = this.playerPlaylist.videoIds[0];
                    } else { // Als niet in loop-modus, dan zijn alle video's bekeken
                        this.playerPlaylistInfo.nextVideoId = '';
                    }
                } else { // Als de laatste video van de afspeellijst niet wordt bekeken, neem de volgende video
                    this.playerPlaylistInfo.nextVideoId = this.playerPlaylist.videoIds[this.playerPlaylist.videoIds.indexOf(currentVideoId) + 1];
                }
            }
        },
        acknowledgeNewVideo(videoId) {
            // Verwijder nieuwe video uit de lijst van de niet-bekeken video's
            let i = this.playerPlaylistInfo.notWatchedVideoIds.indexOf(videoId);
            if (i > -1) this.playerPlaylistInfo.notWatchedVideoIds.splice(i, 1);

            // Bereken de video om te bekijken na deze nieuwe video
            this.calculateNextVideoId(videoId);
        }
    },
    mounted() {
        this.setPlaylistId(this.$route.query.lijst ?? '', this.currentVideoId);
    },
    watch: {
        $route(to) {
            if (to.name == 'Video') { // Als op videopagina...
                if (this.playerPlaylistInfo.playlistId == to.query.lijst) { // Als de afspeellijst niet veranderd...
                    if (to.params.videoId != this.currentVideoId) this.acknowledgeNewVideo(to.params.videoId) // Als de video wel veranderd...
                } else { // Als andere afspeellijst...
                    this.setPlaylistId(to.query.lijst ?? '', to.params.videoId);
                }
            }
        },
        currentVideoId() {
            if (!this.isOnVideoPage) {
                if (this.currentVideoId != '') this.acknowledgeNewVideo(this.currentVideoId);
            }
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
                }
                &.playing {
                    background-color: rgba(255, 255, 255, .05);
                    .thumb {
                        img { filter: brightness(.4); }
                        svg.playIcon { display: block; }
                    }
                }

                & > :first-child {
                    display: flex;
                    align-items: center;
                    padding: 20px;
                    width: 100%;
                    background: transparent;
                    border: none;
                    outline-offset: -2px;
                    font-size: 1em;
                    cursor: pointer;

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
                        text-align: left;
                    }
                }
            }
        }
    }
</style>