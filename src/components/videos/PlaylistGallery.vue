<template>
    <section id="playlistGallery" aria-labelledby="playlistGalleryTitle">
        <div class="container" ref="playlistGalleryContainer">
            <h2 id="playlistGalleryTitle">Afspeellijsten</h2>
            <div class="playlistGalleryMain">
                <button class="playlistGalleryScrollBtn back icon" @click="scroll(true)" tabindex="-1" aria-label="Naar links scrollen"></button>
                <ul ref="playlistGalleryList" aria-labelledby="playlistGalleryTitle">
                    <li :key="playlist" v-for="playlist in playlists" :style="{width: `${this.cardWidthPx}px`}">
                        <PlaylistCard :playlist="playlist" :videos="videos" />
                    </li>
                </ul>
                <button class="playlistGalleryScrollBtn forward icon" @click="scroll(false)" tabindex="-1" aria-label="Naar rechts scrollen"></button>
            </div>
        </div>
    </section>
</template>

<script>
import PlaylistCard from './PlaylistCard.vue'

export default {
    name: 'PlaylistGallery',
    components: { PlaylistCard },
    props: {
        playlists: Array,
        videos: Object
    },
    data() {
        return {
            cardWidthPx: 0,
            cardsVisible: 0
        }
    },
    methods: {
        resizeBody() {
            // Bereken kaartbreedte
            const CONTAINERWIDTH = this.$refs.playlistGalleryContainer.clientWidth;
            const CARD_MIN_WIDTH_PX = 240; // Minimumbreedte van één enkele "afspeellijstkaart"
            this.cardsVisible = Math.max(1, Math.floor(CONTAINERWIDTH / CARD_MIN_WIDTH_PX));
            this.cardWidthPx = CONTAINERWIDTH / this.cardsVisible - 40;
        },
        scroll(isForward) {
            const $list =  this.$refs.playlistGalleryList;
            const CURRENT_VISIBLE_CHILD_INDEX = Math.floor($list.scrollLeft / (this.cardWidthPx + 40));
            const SCROLL_TO_CHILD_INDEX = Math.max(0, Math.min(CURRENT_VISIBLE_CHILD_INDEX + this.cardsVisible * (isForward ? -1 : 1), this.playlists.length - 1));
            const SCROLL_TO_CHILD = $list.children[SCROLL_TO_CHILD_INDEX];
            $list.scrollLeft = Math.max(0, SCROLL_TO_CHILD.offsetLeft - 20);
        }
    },
    mounted() {
        window.addEventListener('resize', this.resizeBody);
        this.resizeBody();
    },
    unmounted() {
        window.removeEventListener('resize', this.resizeBody);
    }
}
</script>

<style lang="scss" scoped>
    #playlistGallery {
        padding-top: 100px;
        background-color: $sectionBackgroundDark;

        .container {
            position: relative;

            h2 { margin-bottom: 30px; }
            .playlistGalleryMain { position: relative; }
            .playlistGalleryScrollBtn {
                position: absolute;
                top: 50%;
                left: -25px;
                transform: translateY(-50%);
                width: 40px;
                height: 40px;
                background: $sectionBackgroundDarker;
                border: 1px solid rgba(0, 0, 0, .2);
                box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, .3);
                border-radius: 50%;
                z-index: 5;

                &::before {
                    content: '';
                    position: relative;
                    display: block;
                    width: 10px;
                    height: 10px;
                    left: 50%;
                    transform: translateX(-25%) rotate(-135deg);
                    border-top: 1px solid gray;
                    border-right: 1px solid gray;
                }

                &.forward {
                    left: unset;
                    right: -25px;

                    &::before { transform: translateX(-75%) rotate(45deg); }
                }
            }
            ul {
                list-style: none;
                height: 360px;
                white-space: nowrap;
                overflow-y: hidden;
                overflow-x: scroll;
                scroll-behavior: smooth;

                li {
                    display: inline-block;
                    box-sizing: border-box;
                    height: calc(100% - 50px);
                    margin: 25px 20px;
                }
            }
        }
    }

    @media screen and (max-width: 600px) {
        #playlistGalleryTitle {
            text-align: center;
            font-size: 2em;
        }
    }
</style>