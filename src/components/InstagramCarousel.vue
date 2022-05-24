<template>
    <div id="instagramCarousel" v-if="mediaList">
        <div id="igcDragOverlay" v-if="isDragging && !isTouchDragging" @mousemove="drag" @mouseup="endDrag" />
        <div id="igcContentWindow">
            <transition :name="isSlideDirectionLeft ? 'slide-left' : 'slide-right'" mode="out-in" @after-enter="actualiseIndices(this.newCurrentMediaIndex)" @leave-cancelled="this.newCurrentMediaIndex = this.currentMediaIndex">
                <div id="igcContent" :key="newCurrentMediaIndex" :class="{'dragging': this.isDragging}" :style="{'--dragTranslateFrac': `${this.dragTranslateFrac}%`}" @mousedown.prevent="this.isStartingDrag = true" @mousemove="startDrag" @mouseup="this.isStartingDrag = false" @pointermove="pointerDrag" @pointerup="endDrag">
                    <div id="igcContentPrev">
                        <img v-if="mediaList[prevMediaIndex].media_type == 'IMAGE'" :src="mediaList[prevMediaIndex].media_url" :alt="caption">
                        <img v-else :src="mediaList[prevMediaIndex].thumb" :alt="caption">
                    </div>
                    <div id="igcContentCurrent">
                        <img v-if="mediaList[currentMediaIndex].media_type == 'IMAGE'" :src="mediaList[currentMediaIndex].media_url" :alt="caption">
                        <InstagramVideo v-else :media="mediaList[currentMediaIndex].media_url" :thumb="mediaList[currentMediaIndex].thumb" :alt="caption" :isDisabled="currentMediaIndex != newCurrentMediaIndex"></InstagramVideo>
                    </div>
                    <div id="igcContentNext">
                        <img v-if="mediaList[nextMediaIndex].media_type == 'IMAGE'" :src="mediaList[nextMediaIndex].media_url" :alt="caption">
                        <img v-else :src="mediaList[nextMediaIndex].thumb" :alt="caption">
                    </div>
                </div>
            </transition>
        </div>
        <button id="igcPrev" class="icon" @click.stop="viewPrev" title="Vorige slide" aria-label="Vorige slide"></button>
        <ul id="igcNav" aria-label="Post navigatie">
            <li
                :key="i"
                v-for="(_, i) in mediaList"
                :class="['igcNavItem', 'icon', { 'active': i === newCurrentMediaIndex }]">
                <button class="icon" @click="viewMedia(i, i > this.currentMediaIndex)" :aria-label="`Post ${i+1}`"></button>
            </li>
        </ul>
        <button id="igcNext" class="icon" @click.stop="viewNext" title="Volgende slide" aria-label="Volgende slide"></button>
    </div>
</template>

<script>
import InstagramVideo from './InstagramVideo.vue'

export default {
    name: 'InstagramCarousel',
    components: {
        InstagramVideo
    },
    props: {
        mediaList: Object,
        caption: String
    },
    data() {
        return {
            prevMediaIndex: 0, // vorige media index
            currentMediaIndex: 0, // huidige media index
            newCurrentMediaIndex: 0,  // (huidige) media index die na een overgang zichtbaar zal zijn
            nextMediaIndex: 1, // volgende media index
            isSlideDirectionLeft: false,
            isStartingDrag: false,
            isDragging: false,
            isTouchDragging: false,
            dragStartX: 0,
            dragTranslateFrac: 0
        }
    },
    methods: {
        viewMedia(index, isSlideDirectionLeft) {
            // Zet nieuwe huidige media index
            this.newCurrentMediaIndex = index;

            this.isSlideDirectionLeft = isSlideDirectionLeft;
            if (this.isSlideDirectionLeft) {
                this.nextMediaIndex = index;
                if (this.nextMediaIndex == this.mediaList.length) this.nextMediaIndex = 0;
            } else {
                this.prevMediaIndex = index;
                if (this.prevMediaIndex == -1) this.prevMediaIndex = this.mediaList.length - 1;
            }
        },
        viewPrev() {
            let index = this.newCurrentMediaIndex - 1;
            if (index == -1) index = this.mediaList.length - 1;
            this.viewMedia(index, false)
        },
        viewNext() {
            let index = this.newCurrentMediaIndex + 1;
            if (index == this.mediaList.length) index = 0;
            this.viewMedia(index, true)
        },
        actualiseIndices(currentIndex) { // Zet vorige, huidige en volgende index van media
            // Zet nieuwe huidige index
            this.currentMediaIndex = currentIndex;
            // Zet nieuwe vorige index
            this.prevMediaIndex = currentIndex - 1;
            if (this.prevMediaIndex == -1) this.prevMediaIndex = this.mediaList.length - 1;
            // Zet nieuwe volgende index
            this.nextMediaIndex = currentIndex + 1;
            if (this.nextMediaIndex == this.mediaList.length) this.nextMediaIndex = 0;

            // Reset dragTranslateFrac
            this.dragTranslateFrac = 0;
        },
        startDrag(e) {
            if (!this.isStartingDrag) return; // Negeer als niet begonnen met slepen
            this.isStartingDrag = false;
            this.isDragging = true;
            this.dragStartX = e.clientX;
            this.dragTranslateFrac = 0;
            if (!this.isTouchDragging) this.$emit('startDragMouse');
        },
        drag(e) {
            this.dragTranslateFrac = Math.atan((this.dragStartX - e.clientX) / 400) * 15;
        },
        endDrag() {
            this.isDragging = false;
            if (this.dragTranslateFrac < -1) {
                this.viewPrev();
            } else if (this.dragTranslateFrac > 1) {
                this.viewNext();
            } else {
                this.dragTranslateFrac = 0;
            }
            if (!this.isTouchDragging) this.$emit('endDragMouse');
            this.isTouchDragging = false;
        },
        pointerDrag(e) {
            if (!this.isTouchDevice()) return; // Negeer als geen touchscreen
            if (!this.isDragging) {
                this.isStartingDrag = true;
                this.isTouchDragging = true;
                this.startDrag(e);
            } else {
                this.drag(e);
            }
        },
        isTouchDevice() {
            return window.matchMedia("(pointer: coarse)").matches // https://stackoverflow.com/a/52855084
        }
    },
    mounted() {
        this.actualiseIndices(0);
    }
}
</script>

<style lang="scss" scoped>
    #instagramCarousel {
        position: relative;
        touch-action: none;
    }
    #instagramCarousel, #igcContentWindow, #igcContent img, #igcContent #instagramVideo {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    #igcContentWindow {
        position: relative;
        overflow: hidden;
    }
    #igcContent {
        position: relative;
        width: 300%;
        height: 100%;
        transform: translateX(calc(-33.285% - var(--dragTranslateFrac)));

        &.dragging, &.slide-left-enter-active, &.slide-right-enter-active {
            #igcContentPrev, #igcContentNext {
                visibility: visible;
            }
        }

        &.slide-left-enter-active, &.slide-right-enter-active {
            transition: transform .25s ease-in-out;
        }
        &.slide-left-enter-to {
            transform: translateX(-66.6%);
        }
        &.slide-right-enter-to {
            transform: translateX(0);
        }
    }
    #igcContentPrev, #igcContentCurrent, #igcContentNext {
        display: inline-block;
        width: 33.3%;
        height: 100%;
    }
    #igcContentPrev, #igcContentNext {
        visibility: hidden;
    }
    #igcNav {
        display: flex;
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, .4);
        border-radius: 4px;

        li {
            display: block;
            float: left;

            button {
                position: relative;
                float: left;
                width: 25px;
                height: 25px;
                border-radius: 4px;

                &::after {
                    content: '';
                    display: inline-block;
                    position: absolute;
                    left: 50%;
                    transform: translateX(-50%) translateY(-50%);
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background: white;
                }
            }

            &.active button {
                background: rgba(0, 0, 0, .3);
                &::after { background: $accentColor; }
            }
        }
    }
    #igcPrev, #igcNext {
        position: absolute;
        top: 50%;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 1px solid rgba(0, 0, 0, .2);
        background-color: rgba(0, 0, 0, .4);

        &::after {
            content: '';
            display: block;
            position: relative;
            left: 50%;
            width: 6px;
            height: 6px;
            border-right: 1px solid white;
            border-bottom: 1px solid white;
        }

        &:hover {
            background-color: rgba(0, 0, 0, .5);
        }
    }
    #igcPrev {
        left: 20px;
        &::after { transform: translateX(-25%) rotate(135deg); }
    }
    #igcNext {
        right: 20px;
        &::after { transform: translateX(-75%) rotate(-45deg); }
    }
    #igcDragOverlay {
        position: fixed;
        width: 100%;
        height: 100%;
        transform: scale(2);
        cursor: w-resize;
        z-index: 15;
    }
</style>