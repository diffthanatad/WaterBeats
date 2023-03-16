<template>
<div class="container">
  <div class="alert-container">
    <div v-for="alert in alertBox" :key="alert['sensor_type']" class="alert-box">
      <div class="sensor-type">
        <label :style="'color:' + alert['color']">{{ alert['sensor_type'].split("_").join(" ") }}</label>
      </div>
      <div class="center">
        <div class="img-container">
          <img class="sensor-img" :src="Object.values(alert['img_src'])">
        </div>
        <div class="alert-field-container">
          <div class="dropdown-container">
            <select class="alert-field dropdown" id="sensor-id-dropdown" v-model="alertsConfig[alert['sensor_type']]['sensor_id']">
              <option value="0" selected disabled>sensor id</option>
              <option v-for="sensorId in sensorIdList[alert['sensor_type']]" :key="sensorId" :value="sensorId">{{sensorId}}</option>
            </select>
            <select class="alert-field dropdown" id="relation-dropdown" v-model="alertsConfig[alert['sensor_type']]['relation']">
              <option v-for="relation in relationList" :key="relation">{{relation}}</option>
            </select>
          </div>
          <div class="input-container">
            <button class='btn-input' id="btn-inc" @click="decreaseValue(alert['sensor_type']);">-</button>
            <div class="input-data">
              <input class="alert-field" type="number" id="number" v-model="alertsConfig[alert['sensor_type']]['threshold']"/>
            </div>
            <button class='btn-input' id="btn-dec" @click="increaseValue(alert['sensor_type'])">+</button>
          </div>
        </div>
        <div class="btn-add-container">
          <button class="btn btn-primary" @click="onAddAlert(alert['sensor_type'])">Add</button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>


<script>
import store from "@/store"
import img_temperature from "@/assets/icon/icon_temperature.jpeg"
import img_soil_moisture from "@/assets/icon/icon_soil_moisture.png"
import img_water_level from "@/assets/icon/icon_water_level.png"
import img_pollution from "@/assets/icon/icon_water_pollution.png"
import { getAllLatest, } from '@/services/sensorService'
import { addAlert, getAlertBySensorId, updateAlertBySensorId } from '@/services/alertService'

export default {
  name: 'FormAlertSetting',
  store,
  data() {
    return {
      alertsConfig: { temperature: { sensor_id: "0", relation: ">", threshold: 0 },
                      soil_moisture: { sensor_id: "0", relation: ">", threshold: 0 },
                      water_level: { sensor_id: "0", relation: ">", threshold: 0 },
                      water_pollution: { sensor_id: "0", relation: ">", threshold: 0 }
      },
      alertBox: [{ img_src: {img_temperature}, sensor_type:"temperature", color:"#F80000" },
                 { img_src: {img_soil_moisture}, sensor_type: "soil_moisture", color: "#01286f" },
                 { img_src: {img_water_level}, sensor_type: "water_level", color: "#65a2fe" },
                 { img_src: {img_pollution}, sensor_type: "water_pollution", color: " #2deca4" }
      ],
      sensorIdList: {temperature: [], soil_moisture: [], water_level: [], water_pollution: []},
      relationList: [">", "<", ">=", "<=", "=="]
    }
  },
  methods: {
    increaseValue(sensorType) {
      this.alertsConfig[sensorType]['threshold'] += 1
    },
    decreaseValue(sensorType) {
      this.alertsConfig[sensorType]['threshold'] -= 1
    },
    async setSensorIdList() {
      const response = await getAllLatest()

      if (response.status !== 200) {
          return
      }
      const sensorList = response.data.data

      for (let sensor of sensorList.values()) {
        if (sensor["type"] === "temperature") {
          this.sensorIdList["temperature"].push(sensor["id"])
        }
        else if(sensor["type"] === "soil_moisture") {
          this.sensorIdList["soil_moisture"].push(sensor["id"])
        }
        else if(sensor["type"] === "water_level") {
          this.sensorIdList["water_level"].push(sensor["id"])
        }
        else if(sensor["type"] === "water_pollution") {
          this.sensorIdList["water_pollution"].push(sensor["id"])
        }
      }
    },
    async addAlert(sensorId, sensorType, threshold, relation) {
      const response = await addAlert(
        sensorId,
        sensorType,
        threshold,
        relation
      )

      if (response.status !== 200) {
        return
      }
    },
    async updateAlert(sensorId, threshold, relation) {
      const response = await updateAlertBySensorId(sensorId, threshold, relation)

      if (response.status !== 200) {
        return
      }
    },
    async resetAlertBox(sensorType) {
      this.alertsConfig[sensorType]['sensor_id'] = "0"
      this.alertsConfig[sensorType]['relation'] = ">"
      this.alertsConfig[sensorType]['threshold'] = 0
    },
    async onAddAlert(sensorType) {

      const sensorId = this.alertsConfig[sensorType]['sensor_id']
      const threshold = this.alertsConfig[sensorType]['threshold']
      const relation = this.alertsConfig[sensorType]['relation']

      if (sensorId == 0) {
        return
      }
      const response = await getAlertBySensorId(sensorId)

      if (response.data.data.length === 0) {
        await this.addAlert(sensorId, sensorType, threshold, relation)
      }
      else {
        await this.updateAlert(sensorId, threshold, relation)
      }
      await store.dispatch('alerts/updateAlertList')
      this.resetAlertBox(sensorType)
    }
  },
  created() {
    this.setSensorIdList()
  }
}
</script>


<style scoped>

#relation-dropdown {
 width: 55px;
}

#sensor-id-dropdown {
  width: 125px
}

#btn-dec {
  border-top-right-radius:  5px;
  border-bottom-right-radius: 5px;
}

#btn-inc {
  border-top-left-radius:  5px;
  border-bottom-left-radius: 5px;
}

.dropdown {
  border: 1px solid #ddd;
  border-radius: 5px;
}

input {
  outline: 0 none;
  text-align: center;
  outline-color: transparent;
  font-size: 18px;
  color: #495057;
}

.alert-box {
  border-radius: 25px;
  border: 2px solid #888888;
  box-shadow: 5px 10px #888888;
  width: 280px;
  height: 355px;
}

.alert-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 45px;
}


.alert-field {
  color: #495057;
  height: 35px;
  text-align: center;
}

.alert-field-container {
  display: flex;
  flex-direction: column;
  padding-top: 27px;
  gap: 10px;
}

.btn {
  font-size: 15px;
}

.btn-add-container {
  display: flex;
  justify-content: center;
  padding-top: 20px;
}

.btn-input {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  border: none;
  width: 30px;
  height: 35px;
}

.btn-input:hover {
  background-color: #dee2e6;
}

.btn-primary {
  text-align: center;
  height: 35px;
  width: 60px;
}

.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.dropdown-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  font-size: 15px;
}

.img-container {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  padding-top: 15px;
}

.input-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.sensor-img {
  max-height: 100px;
  border-radius: 10px;
  padding-top: 5px;
}

.sensor-type {
  font-size: 30px;
  padding-top: 10px;
  padding-left: 22px;
  text-transform: capitalize;
}

input#number {
  text-align: center;
  border: none;
  border: 1px solid #ddd;
  margin: 0px;
  height: 35px;
  width: 125px;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

</style>