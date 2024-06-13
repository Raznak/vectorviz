const routes = [
  {
    path: '/',
    name: "Home",
    component: () => import('pages/IndexPage.vue'),
  },
  {
    path: '/vrl',
    name: "VRL",
    component: () => import('pages/VRLPage.vue'),
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
