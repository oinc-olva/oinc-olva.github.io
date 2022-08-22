<template>
    <label class="toggleInput">
        <input type="checkbox" :id="assignedId" class="tiCheckbox" :checked="checked" @change="e => $emit('change', e.currentTarget.checked)">
        <div class="tiSlider"></div>
    </label>
</template>

<script>
export default {
    name: 'ToggleInput',
    props: {
        assignedId: {
            type: String,
            default: ''
        },
        checked: {
            type: Boolean,
            default: false
        }
    },
    emits: [ 'change' ]
}
</script>

<style lang="scss" scoped>
    $size: 24px;
    $dialSizeFrac: .6;
    $borderWidth: 2px;

    .toggleInput {
        display: inline-block;
        position: relative;
        width: #{$size * 2};
        height: $size;
        margin: 0;
        cursor: pointer;

        &:focus-within {
            outline: 2px solid $accentColor;
            outline-offset: 2px;
        }

        .tiCheckbox {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .tiSlider {
            position: absolute;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, .2);
            border: $borderWidth solid $sectionBorderColor;
            border-radius: $size;
            box-sizing: border-box;
            overflow: hidden;
            transition: background-color .1s cubic-bezier(.46,.03,.52,.96);

            &::before {
                content: '';
                position: absolute;
                background-color: $sectionBorderColor;
                width: #{$size * $dialSizeFrac};
                height: #{$size * $dialSizeFrac};
                border-radius: 50%;
                top: #{$size * (1 - $dialSizeFrac) / 2 - $borderWidth};
                left: #{$size * (1 - $dialSizeFrac) / 2 - $borderWidth};
                transition: transform .3s cubic-bezier(.46,.03,.52,.96),
                            background-color .3s cubic-bezier(.46,.03,.52,.96);
            }
        }
    }
    .tiCheckbox:checked + .tiSlider {
        background-color: rgba(200, 200, 200, .2);
        &::before {
            background-color: $headingColorBright;
            transform: translateX(#{$size * ($dialSizeFrac + .5) - $borderWidth})
        }
    }
</style>