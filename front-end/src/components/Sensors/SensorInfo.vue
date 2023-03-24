<template>
  <div>
    <span class="header">Sensor Info:</span>
    <div class="list_container">
      <label class="info">
        Sensor ID: <br> {{ sensorId }} <br><br>
        Sensor Type: <br> {{ sensorType }} <br><br>
        Latest Data: {{ sensorData }} <br><br>
        Unit: {{ sensorUnit }} <br><br>
        Location: {{ sensorLocation[0] }}, {{ sensorLocation[1] }}
      </label>
    </div>
  </div>
</template>

<style scoped>
.header {
  text-decoration: underline;
}

.info {
  padding-top: 10px;
  width: 15vw;
  height: 22vw;
  font-size: .95vw;
}

.list_container {
  white-space: pre-wrap;
}
</style>


<script>
import { mapState } from 'vuex';
import store from "@/store"

export default {
  name: 'SensorInfo',
  store,
  computed: mapState({
    sensorId: state => state.sensors.currentSensorId,
    sensorData: state => state.sensors.currentSensorData,
    sensorUnit: state => state.sensors.currentSensorUnit,
    sensorLocation: state => state.sensors.currentSensorLocation,
    sensorType: state => state.sensors.selectedSensorType
  })
}
</script>