import { createRouter, createWebHistory } from 'vue-router'
import VueCookies from 'vue-cookies'

const routes = [
    { path: '/auth', name: 'AuthSpotify', component: () => import('../components/AuthSpotify.vue'), meta: { auth: false } },
    { path: '/access-token', name: 'AuthToken', component: () => import('../components/AuthToken.vue'), meta: { auth: false } },
    { path: '/searcher', name: 'SongSearcher', component: () => import('../components/SongSearcher.vue'), meta: { auth: true } }

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    let token = VueCookies.get("access-token");

    if ("auth" in to.meta && to.meta.auth && (!token || token == "undefined") && to.name === "AuthSpotify") {
        next({
            name: "AuthSpotify",
        });
    } else if ("auth" in to.meta && !to.meta.auth && token && token != "undefined") {
        next({
            name: "SongSearcher",
        });
    } else if ("auth" in to.meta && to.meta.auth && (!token || token == "undefined")) {
        next({
            path: "/auth",
            query: { redirect: to.fullPath },
        });
    } else {
        next();
    }
});

export default router