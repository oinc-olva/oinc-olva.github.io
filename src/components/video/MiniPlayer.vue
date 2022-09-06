<template>
    <div id="miniplayerInnerWrapper" :class="{ onVideoPage: isOnVideoPage, playlistOpen: isPlaylistOpen }">
        <VideoPlayer :video="playerVideo" :playerPlaylistInfo="playerPlaylistInfo" :videos="videos" :recommendedVideoIds="recommendedVideoIds" :isAutoplay="isAutoplay" :isOnVideoPage="isOnVideoPage" @setCurrentVideoId="videoId => $emit('setCurrentVideoId', videoId)" @close="$emit('close')" />
        <div id="miniplayerTimelineWrapper"><!-- De tijdlijn van de video wordt naar hier geteleporteerd wanneer de minispeler actief is --></div>
        <div id="miniplayerTitle">
            <h2>{{playerVideo.title}}</h2>
            <button v-if="playerPlaylistInfo.playlistId != ''" id="expandPlaylist" class="icon" :title="isPlaylistOpen ? 'Afspeellijst verbergen' : 'Afspeellijst tonen'" @click="isPlaylistOpen = !isPlaylistOpen"></button>
        </div>
        <MountedTeleport to="#playlistContainer" pageName="Video">
            <Playlist :videos="videos" :playlists="playlists" :currentVideoId="playerVideo.id" :playerPlaylistInfo="playerPlaylistInfo" :isOnVideoPage="isOnVideoPage" @setCurrentVideoId="videoId => $emit('setCurrentVideoId', videoId)" />
        </MountedTeleport>
    </div>
</template>

<script>
import VideoPlayer from './VideoPlayer.vue';
import MountedTeleport from './MountedTeleport.vue';
import Playlist from './Playlist.vue';

export default {
    name: 'MiniPlayer',
    emits: [
        'close',
        'setCurrentVideoId'
    ],
    components: {
        VideoPlayer,
        MountedTeleport,
        Playlist
    },
    props: {
        videos: Object,
        playlists: Array,
        playerVideo: Object,
        recommendedVideoIds: Array,
        isAutoplay: Boolean,
        isOnVideoPage: Boolean
    },
    data() {
        return {
            isPlaylistOpen: false,
            playerPlaylistInfo: {
                playlistId: '',
                nextVideoId: '',
                isShuffle: false,
                isLoop: false,
                notWatchedVideoIds: []
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    #miniplayerInnerWrapper {
        display: flex;
        flex-direction: column;
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 400px;
        max-height: 80%;
        box-shadow: 0 0 20px 4px rgba(0, 0, 0, .3);
        z-index: 8;

        &.onVideoPage {
            position: absolute;
            top: 0;
            width: 100%;
            bottom: unset;
            right: unset;

            #miniplayerTitle { display: none; }
        }
        &:not(.onVideoPage) {
            #playlist {
                display: none;
                flex: 1;
                height: 0;
                margin-bottom: 0;
                padding: 10px;
                overflow: hidden;
            }
        }
    }
    #miniplayerTitle {
        display: flex;
        position: relative;
        flex: 0 0 $miniPlayerTitleHeight;
        box-sizing: border-box;
        background-color: #393f50;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        user-select: none;
        z-index: -1;

        h2 {
            display: inline-block;
            flex: 1;
            box-sizing: border-box;
            margin: 0 10px;
            line-height: $miniPlayerTitleHeight;
            white-space: nowrap;
            font-size: .8em;
            color: #a2a9da;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    }
    #expandPlaylist {
        display: inline-block;
        position: relative;
        width: #{$miniPlayerTitleHeight - 16px};
        height: #{$miniPlayerTitleHeight - 16px};
        background-color: rgba(150, 150, 150, .2);
        border-radius: 2px;
        margin: 8px;

        &::before {
            content: '';
            display: block;
            position: absolute;
            top: 50%;
            left: 50%;
            width: #{$miniPlayerTitleHeight - 34px};
            height: #{$miniPlayerTitleHeight - 34px};
            border-right: 1px solid lightgray;
            border-bottom: 1px solid lightgray;
            transform: translateY(calc(-50% - 2px)) translateX(-50%) rotate(45deg);
        }

        &:hover, &:focus {
            background-color: rgba(150, 150, 150, .3);
        }
    }
    #miniplayerInnerWrapper.playlistOpen {
        #expandPlaylist::before {
            transform: translateY(calc(-50% + 2px)) translateX(-50%) rotate(-135deg);
        }
        #playlist {
            display: flex;
        }
    }

    @media screen and (max-width: 440px) {
        #miniplayerInnerWrapper:not(.onVideoPage) {
            width: calc(100% - 24px);
        }
    }
</style>