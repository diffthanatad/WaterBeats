import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GraphView from '../views/GraphView.vue'
import ActuatorConfigurationView from '../views/ActuatorConfigurationView.vue'
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
    path: '/actuator_configuration',
    name: 'ActuatorConfigurationView',
    component: ActuatorConfigurationView
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
