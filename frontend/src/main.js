import { createApp } from 'vue'
import App from './App.vue'
import router from "./router/index";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import the icons you want to use */
import {faMagnifyingGlass, faPlus} from '@fortawesome/free-solid-svg-icons'

/* add the imported icons to the library */
library.add(faMagnifyingGlass, faPlus)

const options = {
    transition: "Vue-Toastification__fade",
    maxToasts: 20,
    newestOnTop: true
}

createApp(App).component('font-awesome-icon', FontAwesomeIcon).use(router).use(Toast, options).mount('#app')