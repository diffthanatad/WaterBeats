<template>
  <div class="graph-tab d-flex justify-content-center">
    <div class="tab">
      <button
        v-for="sensorType in sensorTypeNames"
        :key="sensorType"
        :style="tabColor(sensorType)"
        @click="updateSelected(sensorType)">
        {{ sensorType }}
      </button>
    </div>
  </div>
</template>


<script>
import { mapState } from 'vuex';
import store from "@/store"

export default {
  name: 'TabsGraph',
  store,
  data () {
    return {
      style: ''
    };
  },
  computed: mapState({
    selectedSensorType: state => state.sensors.selectedSensorType,
    sensorTypeNames: state => state.sensors.sensorTypeNames,
  }),
  methods: {
    tabColor(sensorType) {
      let color = (this.selectedSensorType === sensorType) ? "#5cbcac" : "#3fd9b3"
      return 'background-color: ' + color + ';'
    },
    async updateSelected(sensorType) {
      store.commit('sensors/setSensorType', sensorType)

      await store.dispatch('sensors/updateSensorIdList');
      await store.dispatch('sensors/updateChartData')
    }
  }
}
</script>


<style scoped>
* {
  font-family: 'Kumbh Sans', sans-serif;
  text-transform: uppercase;
}

.tab {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  background-color: #3fd9b3;
  overflow: hidden;
  width: 100%;
  height: 25px;
  border: none;
  font-size: 13px;
}

.tab button {
  display: flex;
  border: 1px solid #fff;
  cursor: pointer;
  padding: 14px 16px;
  color: #fff;
  width: 100%;
  justify-content: center;
}
</style>