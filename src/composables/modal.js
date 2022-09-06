import { ref, onMounted, onUnmounted, getCurrentInstance } from 'vue'
import { useGlobalEventListener } from './event';

export default function useModal() {
    const instance = getCurrentInstance();
    const isInputDisabled = ref(false);

    function setInputDisable(bool) {
        isInputDisabled.value = bool;
    }

    const prevFocus = ref(null);
    onMounted(() => {
        prevFocus.value = document.activeElement;
        instance.refs.firstTab.focus();
    });
    onUnmounted(() => {
        prevFocus.value.focus();
    });

    useGlobalEventListener('keydown', e => {
        if (!isInputDisabled.value) {
            if (e.key == 'Tab') {
                // Zorg voor focus trapping als dialoogvenster open
                if (document.activeElement == instance.refs.firstTab && e.shiftKey) {
                    instance.refs.lastTab.focus();
                    e.preventDefault();
                } else if (document.activeElement == instance.refs.lastTab && !e.shiftKey) {
                    instance.refs.firstTab.focus();
                    e.preventDefault();
                }
            } else if (e.key == 'Escape') {
                // Sluit het dialoogvenster als de gebruiker 'escape' indrukt
                instance.emit('close');
            }
        }
    });

    return { setInputDisable };
}