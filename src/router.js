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
function getHeroHeightPx(heroHeight) {
  return heroHeight == 'vh' ? window.innerHeight : heroHeight;
}

async function setupRouter() {
  const videoPaths = await fetchVideoPaths()

  const routes = [
    {
      path: '/:badPath(.*)*',
      name: '404',
      component: Nietgevonden,
      meta: {
        heroBackground: 'https://images.pexels.com/photos/1655817/pexels-photo-1655817.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260',
        heroHeight: 400
      }
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        heroHeight: 'vh'
      }
    },
    {
      path: '/videos',
      name: 'Video\'s',
      component: Videos,
      meta: {
        heroBackground: "/generated/img/web/banner_youtube.webp",
        heroHeight: 400
      }
    },
    {
      path: '/over-ons',
      name: 'Over ons',
      component: About,
      meta: {
        heroBackground: "/generated/img/web/overons.webp",
        heroHeight: 400
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
            path: `/videos/:videoId/:videoPath`,
            params: {
              videoId: to.params.videoId,
              videoPath: pathObj.path
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
      path: '/videos/:videoId/:videoPath',
      name: 'Video',
      component: Video,
      meta: {
        heroHeight: 0
      },
      beforeEnter: (to, _, next) => {
        if (!videoPaths.hasOwnProperty(to.params.videoId)) {
          return next({
            name: '404',
            params: { badPath: to.path.split('/').slice(1) },
            query: to.query,
            hash: to.hash,
          });
        } else if (videoPaths[to.params.videoId].path !== to.params.videoPath) {
          return next({
            name: 'Video',
            path: `/videos/:videoId/:videoPath`,
            params: {
              videoId: to.params.videoId,
              videoPath: videoPaths[to.params.videoId].path
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
  
  router.beforeEach((to, from, next) => {
    if (to.name == 'Video' && videoPaths.hasOwnProperty(to.params.videoId)) {
      document.title = videoPaths[to.params.videoId].title + ' - OINC'
    } else if (to.name == 'Home') {
      document.title = 'OINC - OLVA\'s Informatie, Nieuws en Cultuur'
    } else {
      document.title = to.name ? to.name + ' - OINC' : 'OINC - OLVA\'s Informatie, Nieuws en Cultuur'
    }

    if (to.path !== from.path) {
      let heroHeightPx = getHeroHeightPx(from.meta.heroHeight);
      if (window.scrollY > heroHeightPx) window.scrollTo({ top: heroHeightPx });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    next()
  })
  return router
}

export default setupRouter