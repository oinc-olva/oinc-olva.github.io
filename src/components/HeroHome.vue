<template>
    <div id="homeVideoslideshow" v-if="videos">
        <transition name="fade" mode="in-out">
            <div class="vssThumb" :style="`top: ${this.scrollOffset}px`" :key="currentId">
                <img :src="videos[currentId].thumbmaxres" :alt="`Thumbnail van video '${videos[currentId].title}'`">
            </div>
        </transition>
        <button id="vssPlay" class="icon" @click="playVideo" :aria-label="`Video '${videos[currentId].title}' afspelen`">
            <fa icon="play" />
        </button>
        <h2 id="vssTitle" :key="currentId">{{videos[currentId].title}}</h2>
        <div id="vssNav">
            <button id="vssPrev" class="prevNextBtn icon" @click="prev()" aria-label="Vorige video"><img src="../assets/arrow.svg" alt=""></button>
            <button
                :key="i"
                v-for="(video, i) in videos"
                :class="['vssItem', 'icon', { 'active': i === currentId }]"
                :aria-label="`Video ${i+1}`"
                @click="setSlide(i)">
                <div></div>
            </button>
            <button id="vssNext" class="prevNextBtn icon" @click="next()" aria-label="Volgende video"><img src="../assets/arrow.svg" alt=""></button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HeroHome',
    data() {
        return {
            currentId: 0,
            interval: null,
            scrollOffset: 0,
            isVisible: true
        }
    },
    props: {
        videos: Array
    },
    methods: {
        prev() {
            this.currentId--;
            if (this.currentId == -1) this.currentId = this.videos.length - 1;
            this.setNextInterval();
        },
        next() {
            this.currentId++;
            if (this.currentId == this.videos.length) this.currentId = 0;
            this.setNextInterval();
        },
        setSlide(slide) {
            this.currentId = slide;
            this.setNextInterval();
        },
        setNextInterval() {
            if (this.interval) window.clearInterval(this.interval);
            this.interval = window.setInterval(() => {
                this.next();
            }, 10000);
        },
        playVideo() {
            this.$router.push({
                name: 'Video',
                path: '/videos/:videoId/:videoPath',
                params: {
                    videoId: this.videos[this.currentId].id,
                    videoPath: this.videos[this.currentId].videoPath
                }
            })
        },
        scroll() {
            // Kijk als zichtbaar
            let prevIsVisible = this.isVisible;
            this.isVisible = window.scrollY < window.innerHeight;
            // Zet scroll voor parallax-effect
            if (this.isVisible) this.scrollOffset = -window.scrollY / 3;
            // Als net zichtbaar of net niet zichtbaar
            if (this.isVisible != prevIsVisible) {
                if (this.isVisible) {
                    this.setNextInterval(); // Verander steeds de slide wanneer zichtbaar
                } else {
                    if (this.interval) window.clearInterval(this.interval); // Stop het veranderen van de slide
                }
            }
        }
    },
    mounted: function() {
        this.setNextInterval();
        document.addEventListener('scroll', this.scroll, false);
    },
    unmounted() {
        document.removeEventListener('scroll', this.scroll, false);
    }
}
</script>

<style lang="scss" scoped>
    @use '../mixins/scrim-gradient.scss' as *;
    #homeVideoslideshow {
        position: relative;
        height: 100%;
        padding-bottom: 40px;
        overflow: hidden;

        &.fade-leave-active::after { display: none; }

        &::after {
            content: '';
            position: absolute;
            display: block;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 30%;
            z-index: -1;
            @include scrimGradient(rgba(20, 20, 20, 0.8), 'to top');
        }
    }
    .vssThumb {
        position: fixed;
        pointer-events: none;
        height: 105vh;
        width: 100%;
        overflow: hidden;
        transition: opacity .3s ease-out;
        z-index: -6;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(.55);
            animation: zoom 4s;
            animation-fill-mode: forwards;

            @keyframes zoom {
                from { transform: scale(1); }
                to { transform: scale(1.05); }
            }
        }
        &.fade-enter-from {
            opacity: 0;
        }
    }
    #vssPlay {
        position: absolute;
        top: 50%;
        left: 50%;
        font-size: 20px;
        background: rgba(0, 0, 0, .4);
        width: 70px;
        height: 70px;
        border-radius: 50%;
        border: 1px solid rgba(143, 143, 143, 0.25);
        transform: translateX(-50%) translateY(-50%);
        transition: transform .3s cubic-bezier(.68,-0.55,.27,1.55),
                    background-color .3s ease-in-out,
                    border-color .3s ease-in-out;

        &:hover, &:active, &:focus {
            transform: translateX(-50%) translateY(-50%) scale(1.2);
            background-color: rgba(0, 0, 0, .7);
            border-color: $accentColor;
        }
        &:focus:focus-visible { border: none; }
    }
    #vssTitle {
        position: absolute;
        font-size: calc((6vh + 4vw) / 2);
        width: 100%;
        bottom: 0;
        color: white;
        text-align: center;
        box-sizing: border-box;
        padding: 10px;
        padding-bottom: 125px;
    }
    #vssNav {
        position: absolute;
        display: flex;
        align-items: center;
        bottom: 60px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, .3);
        border: 1px solid rgba(143, 143, 143, 0.25);
        border-radius: 50px;
        z-index: 8;

        .prevNextBtn {
            position: relative;
            padding: 10px;
            margin: 0 15px;
            font-size: 0;

            img {
                width: 15px;
                height: 15px;
            }
            &#vssNext {
                transform: rotate(180deg);
            }
        }
        .vssItem {
            width: 19px;
            margin: 0 3px;
            padding: 0 2px;
            box-sizing: content-box;

            div {
                position: relative;
                width: 15px;
                height: 15px;
                border: 2px solid white;
                border-radius: 50%;
                margin: 10px 0;
        
                &::after {
                    content: '';
                    position: absolute;
                    display: inline-block;
                    width: 0;
                    height: 0;
                    background-color: white;
                    border-radius: 50%;
                    top: 50%;
                    left: 50%;
                    transform: translateX(-50%) translateY(-50%);
                    transition: width .2s ease-in-out, height .2s ease-in-out;
                }
            }
            &.active div::after {
                width: 50%;
                height: 50%;
            }
        }
    }
</style>