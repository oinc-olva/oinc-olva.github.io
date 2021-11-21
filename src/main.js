import { createApp } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faExternalLinkAlt, faTimes, faPause, faPlay, faVolumeMute, faVolumeOff, faVolumeDown, faVolumeUp } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import App from './App.vue'
import setupRouter from './router'

library.add(fab, faExternalLinkAlt, faTimes, faPause, faPlay, faVolumeMute, faVolumeOff, faVolumeDown, faVolumeUp);

setupRouter().then(router =>
    createApp(App)
        .use(router)
        .component('fa', FontAwesomeIcon)
        .mount('#app')
);
