import { createApp } from 'vue'
import App from './App.vue'
import setupRouter from './router'

setupRouter().then(router => createApp(App).use(router).mount('#app'));
