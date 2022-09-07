import { onMounted, onUnmounted } from 'vue'

export function useGlobalEventListener(event, callback) {
    onMounted( () => document.addEventListener(event, callback) );
    onUnmounted( () => document.removeEventListener(event, callback) );
}