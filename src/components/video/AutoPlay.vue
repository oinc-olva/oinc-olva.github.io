<template>
    <div id="autoPlay">
        <ToggleInput assignedId="autoPlaySetting" :checked="isAutoplay" @change="isChecked => $emit('setAutoplay', isChecked)" />
        <label for="autoPlaySetting">Autoplay</label>
    </div>
</template>

<script>
import ToggleInput from './ToggleInput.vue';

export default {
    name: 'AutoPlay',
    emits: [ 'setAutoplay' ],
    components: {
        ToggleInput
    },
    props: {
        isAutoplay: Boolean
    }
}
</script>

<style lang="scss" scoped>
    #autoPlay {
        display: flex;
        background: $sectionBackgroundDarker;
        border: 1px solid $sectionBorderColor;
        border-radius: 4px;
        margin-bottom: 20px;
        padding: 20px;
    }
    label {
        margin-left: 20px;
        color: $textColor;
    }
</style>