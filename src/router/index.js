import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Videos from '../views/Videos.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'
import Video from '../views/Video.vue'
import Nietgevonden from '../views/Nietgevonden.vue'

async function fetchVideoPaths() {
  const res = await fetch('/videopaths.json')
  const data = await res.json()
  return data
}
async function setupRouter() {
  const videoPaths = await fetchVideoPaths()

  const routes = [
    {
      path: '/:badpath(.*)',
      redirect: to => {
        return {
          name: 'Pagina niet gevonden!',
          path: '/nietgevonden',
          query: { p: to.params.badpath }
        }
      }
    },
    {
      path: '/nietgevonden',
      name: 'Pagina niet gevonden!',
      component: Nietgevonden,
      meta: {
        heroBackground: 'url(\'https://images.pexels.com/photos/1655817/pexels-photo-1655817.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260\')'
      }
    },
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
    },
    {
      path: '/videos/:videoId',
      name: 'Video-omleiding',
      redirect: to => {
        let path = videoPaths[to.params.videoId]
        if (path) {
          return {
            name: 'Video',
            path: `/videos/:videoId/:videoName`,
            params: {
              videoId: to.params.videoId,
              videoName: path
            }
          }
        } else {
          return {
            name: 'Pagina niet gevonden!',
            path: '/nietgevonden',
            query: { p: 'videos/' +  to.params.videoId }
          }
        }
      }
    },
    {
      path: '/videos/:videoId/:videoName',
      name: 'Video',
      component: Video,
      beforeEnter: (to, _, next) => {
        if (!videoPaths.hasOwnProperty(to.params.videoId)) {
          return next({
            name: 'Pagina niet gevonden!',
            path: '/nietgevonden',
            query: { p: `videos/${to.params.videoId}/${to.params.videoName}` }
          });
        } else if (videoPaths[to.params.videoId] !== to.params.videoName) {
          return next({
            name: 'Video',
            path: `/videos/:videoId/:videoName`,
            params: {
              videoId: to.params.videoId,
              videoName: videoPaths[to.params.videoId]
            }
          });
        }
        next()
      }
    }
  ]
  
  const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
  })
  
  router.beforeEach((to, _, next) => {
    document.title = to.name ? 'OINC | ' + to.name : 'OINC'
    window.scrollTo({ top: 0, behavior: 'smooth' });
    next()
  })
  return router
}

export default setupRouter