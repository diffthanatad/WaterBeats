import { createStore } from 'vuex'
import alerts from './alerts.js'
import device from './device.js'
import sensors from './sensors.js'

export default createStore({
  modules: {
    alerts,
    device,
    sensors
  }
})
