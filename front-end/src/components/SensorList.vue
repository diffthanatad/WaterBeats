<template>
  <div>
    <span class="header">Sensor ID List:</span>
    <div class="list_container">
      <select class="list" multiple>
        <option class="item" v-for="sensorId in sensorIdList" :key="sensorId" @click="handleClicks($event);">
          {{sensorId}}
        </option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.header {
  font-size: 1.1vw;
  text-decoration: underline;
}

.list_container {
  padding-bottom: 20px;
}

.list {
  width: 15vw;
  height: 22vw;
  border-color: #cbd1e0;
  font-size: 1.1vw;
}

.item:hover {
  background-color: #b3d7ff;
}

</style>

<script setup>
import { defineExpose } from 'vue'

function childMethod() {
  this.updateSensorList()
}

defineExpose({ childMethod })
</script>

<script>
import {tabSelect} from "@/store/tab-select.js"
import {chart} from "@/store/chart-data"
import {getAllLatest} from '@/services/sensorService.js'

export default {
  name: 'SensorList',
  expose: ["updateSensorList"],
  props: ["updateLineGraph", "updateSensorInfo"],
  components: {},
  data() {
    return  {
      sensorIdList: [],
      style: ""
    }
  },
  methods: {
    updateSensorIdStore(sensorId) {
      sensorId = (sensorId === undefined) ? "" : sensorId
      chart.value.setSensorId(sensorId)
    },
    async updateSensorList() {
      const response = await getAllLatest()

      if (response.status !== 200) {
        this.updateSensorIdStore("")
        this.sensorIdList = []
        return
      }

      let sensorIds = []
      const sensorsList = response.data.data
      const selectedTabName = tabSelect.value.selectedTab

      for (let sensor of sensorsList.values()) {
        if (sensor["sensor_type"] == selectedTabName) {
          sensorIds.push(sensor["sensor_id"])
        }
      }
      // Assign the first sensor ID to 'sensorId' in @/store/chat-data.js
      this.updateSensorIdStore(sensorIds[0])
      this.sensorIdList = sensorIds

      await this.updateLineGraph()
      await this.updateSensorInfo()
    },
    async handleClicks(click) {
      chart.value.setSensorId(click.target.innerHTML)

      await this.updateLineGraph()
      await this.updateSensorInfo()
    }
  },
  async created() {
    await this.updateSensorList()
  }
}
</script>