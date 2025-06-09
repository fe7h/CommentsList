import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'

import store from "./store"
import { install } from "vue3-recaptcha-v2"

const app = createApp(App)
app.use(store)
app.use(install, {
    sitekey: "6LeHL1krAAAAAIWnsEZvdfhd2uFM7lRBPYITvnac",
  })
app.mount('#app')
