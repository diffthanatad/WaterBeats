<template>
  <div>
    <span class="header">Sensor ID List:</span>
    <div class="sensor-list-container">
      <select class="sensor-list" id="sensor-list" multiple>
        <option class="item" v-for="sensorId in sensorIdList" :key="sensorId" @click="handleClicks()">
          {{ sensorId }}
        </option>
      </select>
    </div>
  </div>
</template>


<script>
import { mapState } from 'vuex';
import store from "@/store"

export default {
  name: 'SensorList',
  store,
  computed: mapState({
    sensorIdList: state => state.sensors.sensorIdList,
  }),
  methods: {
    async handleClicks() {
      let selected = []

      for (var option of document.getElementById('sensor-list').options) {
        if (option.selected) {
          selected.push(option.value);
        }
      }
      if (selected.length === 1) {
        store.commit('sensors/setSensorId', selected[0])
        await store.dispatch('sensors/updateChartData')
      }
      else {
        store.commit('sensors/setSelectedSensorIdList', selected)
        await store.dispatch('sensors/updateChartDataMultiple')
        store.commit('sensors/RESET_SENSOR_LIST')
      }
    }
  }
}
</script>

<style scoped>

.header {
  font-size: 1.1vw;
  text-decoration: underline;
}

.item:hover {
  background-color: #b3d7ff;
}

.sensor-list {
  width: 15vw;
  height: 22vw;
  border-color: #cbd1e0;
  font-size: 1.1vw;
}

.sensor-list-container {
  padding-bottom: 20px;
}

</style>