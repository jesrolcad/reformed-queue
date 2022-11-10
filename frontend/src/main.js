import { createApp } from 'vue'
import App from './App.vue'
import router from "./router/index";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const options = {
    transition: "Vue-Toastification__fade",
    maxToasts: 20,
    newestOnTop: true
}

createApp(App).use(router).use(Toast, options).mount('#app')