import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.min.js'


import 'leaflet/dist/leaflet.css';

createApp(App).use(store).use(router).mount('#app')
