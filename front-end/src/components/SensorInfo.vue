<template>
  <div>
    <span class="header">Sensor Info:</span>
    <div class="list_container">
      <label class="info" :sensorInfo="sensorInfo">
        {{sensorInfo}}
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


<script setup>
import { defineExpose } from 'vue'

function childMethod() {
  this.updateSensorInfo()
}

defineExpose({ childMethod })
</script>


<script>
import {chart} from "@/store/chart-data"
import {getLatestById} from '@/services/sensorService.js'

export default {
  name: 'SensorInfo',
  expose: ["updateSensorInfo"],
  components: {},
  data() {
    return  {
      sensorInfo: ""
    }
  },
  methods: {
    async updateSensorInfo() {

      const sensorId = chart.value.sensorId
      const response = await getLatestById(sensorId)

      if (response.status !== 200 || sensorId === "") {
        this.sensorInfo = ""
        return
      }
      const info = response.data.data

      let sensorInfo = ""
      sensorInfo += "Sensor ID: \n" + info["sensor_id"] + "\n\n"
      sensorInfo += "Sensor Type: \n" + info["sensor_type"] + "\n\n"
      sensorInfo += "Current Data: " + info["data"].toFixed(2) + "\n\n"
      sensorInfo += "Unit: " + info["unit"] + "\n\n"
      sensorInfo += "Location: " + info["location"] + "\n"

      this.sensorInfo = sensorInfo
    }
  },
  // created() {
  //   this.updateSensorInfo()
  // }
}
</script>