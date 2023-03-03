import { createStore } from 'vuex'
import device from './device.js'

export default createStore({
  modules: {
    device,
  }
})
