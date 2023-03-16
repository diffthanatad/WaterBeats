import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GraphView from '../views/GraphView.vue'
import ActuatorConfigurationView from '../views/ActuatorConfigurationView.vue'
import AdminView from '../views/AdminView.vue'
import SettingView from '../views/SettingView.vue'
import LogInView from '../views/LogInView.vue'
import AlertsView from '../views/AlertsView.vue'

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
  },
  {
    path: '/login',
    name: 'LogIn',
    component: LogInView
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: AlertsView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const authRequired = to.name !== "LogIn";
  const loggedIn = localStorage.getItem('username');
  const adminRoleRequired = to.name === "Admin";
  const role = localStorage.getItem('role');

  if (authRequired && !loggedIn) {
    return next('/login');
  } else if (adminRoleRequired && role !== "ROLE_ADMIN") {
    return next('/');
  } else {
    next();
  }
})

export default router
