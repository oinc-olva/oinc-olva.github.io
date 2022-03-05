import { createApp } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faExternalLinkAlt, faTimes, faPause, faPlay, faVolumeMute, faVolumeOff, faVolumeDown, faVolumeUp, faTachometerAlt, faExpand, faCompress, faShareAlt, faBars } from '@fortawesome/free-solid-svg-icons'
import { faDiscord, faFacebookMessenger, faWhatsapp, faFacebook, faInstagram, faYoutube, faSnapchat, faTiktok, faTwitch, faTwitter, faWix, faWordpress, faSquarespace, faGithub, faGoogle } from '@fortawesome/free-brands-svg-icons'
import App from './App.vue'
import setupRouter from './router.js'

library.add(
    faDiscord, faFacebookMessenger, faWhatsapp, faFacebook, faInstagram, faYoutube, faSnapchat, faTiktok, faTwitch, faTwitter, faWix, faWordpress, faSquarespace, faGithub, faGoogle,
    faExternalLinkAlt, faTimes, faPause, faPlay, faVolumeMute, faVolumeOff, faVolumeDown, faVolumeUp, faTachometerAlt, faExpand, faCompress, faShareAlt, faBars
);

setupRouter().then(router =>
    createApp(App)
        .use(router)
        .component('fa', FontAwesomeIcon)
        .mount('#app')
);
