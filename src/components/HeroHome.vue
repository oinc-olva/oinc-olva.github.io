<template>
    <div class="videoslideshow" v-if="videos">
        <transition name="fade" mode="in-out">
            <div class="vssThumb" :key="currentId">
                <img :src="videos[currentId].thumbmaxres" alt="">
            </div>
        </transition>
        <button id="play" class="icon" @click="playVideo">
            <fa icon="play" />
        </button>
        <h2 class="vssTitle" :key="currentId">{{videos[currentId].title}}</h2>
        <ul class="vssNav">
            <button id="vssPrev" class="icon" @click="prev()"><img src="../assets/arrow.svg" alt=""></button>
            <li
                :key="i"
                v-for="(video, i) in videos"
                :class="{ 'active': i === currentId }"
                @click="setSlide(i)"
            />
            <button id="vssNext" class="icon" @click="next()"><img src="../assets/arrow.svg" alt=""></button>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'HeroHome',
    data() {
        return {
            currentId: 0,
            interval: null
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
                path: '/videos/:videoId/:videoName',
                params: {
                    videoId: this.videos[this.currentId].id,
                    videoName: this.videos[this.currentId].videoPath
                }
            })
        }
    },
    mounted: function() {
        this.setNextInterval();
    }
}
</script>

<style lang="scss" scoped>
    @use '../mixins/scrim-gradient.scss' as *;
    .videoslideshow {
        position: relative;
        height: 100%;
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
        height: 100%;
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
    #play {
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

        &:hover {
            transform: translateX(-50%) translateY(-50%) scale(1.2);
            background-color: rgba(0, 0, 0, .7);
            border-color: $accentColor;
        }
    }
    .vssTitle {
        position: absolute;
        font-size: calc(100vh / 15);
        width: 100%;
        bottom: 0;
        color: white;
        text-align: center;
        padding: 20px 0 calc(100vh / 14 + 20px);
    }
    .vssNav {
        position: absolute;
        display: flex;
        align-items: center;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, .3);
        border: 1px solid rgba(143, 143, 143, 0.25);
        border-radius: 50px;
        z-index: 8;

        li {
            position: relative;
            display: inline-block;
            width: 15px;
            height: 15px;
            border: 2px solid white;
            border-radius: 50%;
            margin: 0 5px;
            cursor: pointer;

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
            &.active::after {
                width: 50%;
                height: 50%;
            }
        }

        button {
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
    }
</style>