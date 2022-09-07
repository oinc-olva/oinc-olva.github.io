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
        // CSS selector voor het element waarnaar er wordt geteleporteerd
        to: {
            type: String,
            default: 'body'
        },
        // Als disabled==false, dan zal het element niet worden geteleporteerd (ongeacht als wel/niet op juiste pagina)
        disabled: {
            type: Boolean,
            default: false
        },
        // Paginanaam waarop het element (niet) moet komen
        pageName: {
            type: String,
            default: ''
        },
        // Als inverted==false, dan wordt het element enkel geteleporteerd als op pagina 'pageName'.
        // Als inverted==true, dan wordt het element geteleporteerd als niet op pagina 'pageName'.
        inverted: {
            type: Boolean,
            default: false
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
                if ((route.name == this.pageName) != this.inverted) { // XOR(route.name == this.pageName, this.inverted)
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