import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {path: '/auth', name:'AuthSpotify', component: () => import('../components/AuthSpotify.vue')},
    {path: '/access-token', name:'AuthToken', component: () => import('../components/AuthToken.vue')},
    {path: '/searcher', name:'SongSearcher', component: () => import('../components/SongSearcher.vue')}

    ]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router