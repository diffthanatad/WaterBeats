import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GraphView from '../views/GraphView.vue'
import ConfigurationView from '../views/ConfigurationView.vue'
import AdminView from '../views/AdminView.vue'
import SettingView from '../views/SettingView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/graph',
    name: 'Graph',
    component: GraphView
  },
  {
    path: '/configuration',
    name: 'Configuration',
    component: ConfigurationView
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView
  },
  {
    path: '/setting',
    name: 'Setting',
    component: SettingView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
