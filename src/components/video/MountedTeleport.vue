<template>
    <teleport v-if="isMounted && (target || !isOnPage)" :to="isOnPage ? to : 'html'" :disabled="!isOnPage || !target || disabled">
        <slot></slot>
    </teleport>
</template>

<script>
import { ref } from 'vue';

export default {
    name: "MountedTeleport",
    props: {
        to: {
            type: String,
            default: 'body'
        },
        disabled: {
            type: Boolean,
            default: false
        },
        pageName: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            isMounted: false,
            isOnPage: false
        }
    },
    methods: {
        reloadTarget(route) {
            this.$nextTick(() => {
                if (route.name == this.pageName) {
                    this.isOnPage = true;
                    const el = document.querySelector(this.to);
                    if (el) this.target = el;
                } else {
                    this.isOnPage = false;
                    this.target = null;
                }
            });
        }
    },
    setup() {
        const target = ref(null);
        return { target }
    },
    mounted() {
        this.isMounted = true;
        this.reloadTarget(this.$route);
    },
    watch: {
        $route(dest) {
            this.reloadTarget(dest);
        }
    }
}
</script>