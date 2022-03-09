import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Videos from './views/Videos.vue'
import About from './views/About.vue'
import Video from './views/Video.vue'
import Nietgevonden from './views/Nietgevonden.vue'

async function fetchVideoPaths() {
  const res = await fetch('/generated/data/videopaths.json')
  const data = await res.json()
  return data
}
async function setupRouter() {
  const videoPaths = await fetchVideoPaths()

  const routes = [
    {
      path: '/:badPath(.*)*',
      name: '404',
      component: Nietgevonden,
      meta: {
        heroBackground: 'https://images.pexels.com/photos/1655817/pexels-photo-1655817.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260'
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
        heroBackground: "/generated/img/web/banner_youtube.jpg"
      }
    },
    {
      path: '/over-ons',
      name: 'Over ons',
      component: About,
      meta: {
        heroBackground: "/generated/img/web/overons.jpg"
      }
    },
    {
      path: '/videos/:videoId',
      name: 'Video-omleiding',
      alias: '/v/:videoId',
      redirect: to => {
        let pathObj = videoPaths[to.params.videoId]
        if (pathObj) {
          return {
            name: 'Video',
            path: `/videos/:videoId/:videoName`,
            params: {
              videoId: to.params.videoId,
              videoName: pathObj.path
            }
          }
        } else {
          return {
            name: '404',
            params: { badPath: to.path.split('/').slice(1) },
            query: to.query,
            hash: to.hash,
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
            name: '404',
            params: { badPath: to.path.split('/').slice(1) },
            query: to.query,
            hash: to.hash,
          });
        } else if (videoPaths[to.params.videoId].path !== to.params.videoName) {
          return next({
            name: 'Video',
            path: `/videos/:videoId/:videoName`,
            params: {
              videoId: to.params.videoId,
              videoName: videoPaths[to.params.videoId].path
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
    if (to.name == 'Video' && videoPaths.hasOwnProperty(to.params.videoId)) {
      document.title = videoPaths[to.params.videoId].title + ' - OINC'
    } else if (to.name == 'Home') {
      document.title = 'OINC'
    } else {
      document.title = to.name ? to.name + ' - OINC' : 'OINC'
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
    next()
  })
  return router
}

export default setupRouter