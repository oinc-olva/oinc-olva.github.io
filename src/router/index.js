import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Videos from '../views/Videos.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/videos',
    name: 'Video\'s',
    component: Videos,
    meta: {
      heroBackground: "url(\"/banner.jpg\")"
    }
  },
  {
    path: '/over-ons',
    name: 'Over ons',
    component: About,
    meta: {
      heroBackground: "url(\"overons.jpg\")"
    }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact,
    meta: {
      heroBackground: "url(\"https://picsum.photos/1000\")"
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
  document.title = to.name ? 'OINC | ' + to.name : 'OINC'
  next()
})

export default router
