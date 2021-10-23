<template>
    <section :class="[{ 'fadeIn': fadeIn }, 'videoslideshow']">
        <ul class="vssVideos">
            <li :key="video" v-for="(video, i) in videos" :class="{ 'active': i === currentId }">
                <img :src="video.thumbmaxres" alt="">
                <h2>{{video.title}}</h2>
            </li>
        </ul>
        <ul class="vssArrows">
            <button class="vssPrev" @click="prev()"><img src="../assets/arrow.svg" alt=""></button>
            <button class="vssNext" @click="next()"><img src="../assets/arrow.svg" alt=""></button>
        </ul>
        <ul class="vssNav">
            <li
                :key="i"
                v-for="(video, i) in videos"
                :class="{ 'active': i === currentId }"
                @click="setSlide(i)"
            />
        </ul>
    </section>
</template>

<script>
export default {
    name: 'Homevideoslides',
    props: {
        videos: Array,
    },
    data() {
        return {
            currentId: 0,
            fadeIn: false,
            interval: null
        }
    },
    methods: {
        prev: function() {
            this.currentId--;
            if (this.currentId == -1) this.currentId = this.videos.length - 1;
            this.fadeIn = false;
            this.setNextInterval();
        },
        next: function() {
            this.currentId++;
            if (this.currentId == this.videos.length) this.currentId = 0;
            this.fadeIn = true;
            this.setNextInterval();
        },
        setSlide: function(slide) {
            this.fadeIn = slide > this.currentId;
            this.currentId = slide;
            this.setNextInterval();
        },
        setNextInterval: function() {
            if (this.interval) window.clearInterval(this.interval);
            this.interval = window.setInterval(() => {
                this.next();
            }, 10000);
        }
    },
    mounted: function() {
        this.setNextInterval();
    }
}
</script>

<style lang="scss" scoped>
    .videoslideshow {
        position: relative;
        height: 100vh;
        background-color: black;
    }
    .vssVideos {
        li {
            position: absolute;
            display: block;
            opacity: 0;
            &.active { opacity: 1; }
            height: 100%;
            overflow: hidden;
            transition: opacity .8s ease-in;

            &, img {
                width: 100%;
            }
            img {
                transform: scale(1);
                pointer-events: none;
                height: 100%;
                object-fit: cover;
                opacity: .7;
                animation: zoom 6s;
                transition: transform 6s ease-in-out;

                @keyframes zoom {
                    from { transform: scale(1); }
                    to { transform: scale(1.1); }
                }
            }
            &.active img { transform: scale(1.1); }
            h2 {
                position: absolute;
                font-size: 2.3em;
                right: 50px;
                bottom: 20px;
                color: white;
                background-color: rgba(0, 0, 0, .5);
                padding: 5px 20px;
            }
        }
    }
    .videoslideshow.fadeIn .vssVideos li:not(.active) { transition-delay: .2s }
    .videoslideshow:not(.fadeIn) .vssVideos li:not(.active) { transition-delay: .2s }
    .vssArrows {
        width: 100%;

        button {
            position: absolute;
            background: rgba(0, 0, 0, .4);
            width: 50px;
            height: 50px;
            border: none;
            border-radius: 50%;
            line-height: 100%;
            top: 50%;
            cursor: pointer;

            &.vssPrev {
                left: 50px;
                transform: translateY(-50%);
            }
            &.vssNext {
                right: 50px;
                transform: translateY(-50%) rotate(180deg);
            }
        }
    }
    .vssNav {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);

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
    }
</style>