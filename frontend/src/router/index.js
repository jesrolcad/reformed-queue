import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {path: '/auth', name:'AuthSpotify', component: () => import('../components/AuthSpotify.vue'), meta: {auth: false}},
    {path: '/access-token', name:'AuthToken', component: () => import('../components/AuthToken.vue'), meta: {auth: true}},
    {path: '/searcher', name:'SongSearcher', component: () => import('../components/SongSearcher.vue'), meta: {auth: true}}

    ]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach( (to, from) => {

    let token = localStorage.getItem('access-token')

    console.log("FROM", from)
    console.log("TO", to)
    console.log('auth' in to.meta && to.meta.auth && (!token || token == 'undefined'))

    //Si se quiere acceder a una ruta que requiere autenticación y no hay token(última condición para evitar login infinito)
    if('auth' in to.meta && to.meta.auth && (!token || token == 'undefined') && to.name === 'AuthSpotify'){ 
        console.log("ENTRA PRIMERA CONDICIÓN")
        return {name: 'AuthSpotify'}
    }else if('auth' in to.meta && !to.meta.auth && token && token != 'undefined'){ //Si no se requiere autenticación y hay token
        console.log("ENTRA SEGUNDA CONDICIÓN")
        return {name: 'SongSearcher'}}
    

});

export default router