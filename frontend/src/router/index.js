import { createRouter, createWebHistory } from 'vue-router'

const routes = [{path: '/prueba', name:'PruebaItem', component: () => import('../components/PruebaItem.vue')}]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router