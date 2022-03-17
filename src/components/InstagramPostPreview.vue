<template>
    <a class="instagramPostPreviewWrapper" :href="post.permalink" target="_blank" :aria-label="`Post met naam '${this.post.caption}'`">
        <div class="instagramPostPreview">
            <div class="thumb" :style="`background: linear-gradient(rgba(0, 0, 0, .1), rgba(0, 0, 0, .1)), url('${post.thumb}')`">
                <div class="foreground">
                    <div class="expand">
                        <fa icon="external-link-alt" />
                    </div>
                </div>
            </div>
            <h4 class="title">
                {{post.title}}
            </h4>
        </div>
    </a>
</template>

<script>
export default {
    name: 'InstagramPostPreview',
    props: {
        post: Object
    }
}
</script>

<style lang="scss" scoped>
    .instagramPostPreviewWrapper {
        position: relative;
        display: block;
        padding: 20px;
    
        &:hover, &:focus:focus-visible {
            .thumb {
                transform: scale(1.1);
            }
            .foreground {
                visibility: visible;
                svg {
                    opacity: 1;
                    transform: translateX(-50%) translateY(-50%);
                }
            }
        }

        .instagramPostPreview {
            display: block;
            overflow: hidden;
            border-radius: 4px;
        }    
        .thumb {
            position: relative;
            width: 100%;
            padding-top: 100%;
            background-size: cover !important;
            transition: transform .3s ease-in-out;
        }
        .foreground {
            position: absolute;
            display: block;
            visibility: hidden;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, .4);
    
            .expand {
                transform: rotate(270deg);
                height: 100%;
            }
            svg {
                position: absolute;
                top: 50%;
                left: 50%;
                color: white;
                font-size: 40px;
                opacity: 0;
                transform: translateX(-50%) translateY(-50%) scale(1.1);
                transition: opacity .2s ease-in-out,
                            transform .3s ease-in-out;
            }
        }
    }
</style>