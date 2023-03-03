<template>
  <div class="containter">
    <div class="instruction">
      <div>
        <h3>Instruction</h3>
      </div>
      <table>
        <tr>
          <td>Target Actuator:</td>
          <td>
            <select class="size" @change="onChangeActuatorType($event)">
              <option value="" selected disabled hidden>actuator type</option>
              <option>sprinkler</option>
              <option>pump</option>
            </select>
          </td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>actuator id</option>
            </select>
          </td>
        </tr>
        <tr>
          <td>State:</td>
          <td>
            <label class="switch">
              <input type="checkbox">
              <div class="slider round">
                <span class="on">ON</span>
                <span class="off">OFF</span>
              </div>
            </label>
          </td>
        </tr>
        <tr>
          <td>Intensity:</td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>percentage</option>
              <option v-for="percentage in getIntensity()" :key="percentage">{{percentage}}</option>
            </select>
          </td>
        </tr>
        <tr>
          <td>Duration:</td>
          <td>
            <input class="size" label="day" placeholder="day/s"/>
          </td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>hours</option>
              <option v-for="hour in getTimeList('hours')" :key="hour">{{hour}}</option>
            </select>
          </td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>minutes</option>
              <option v-for="minutes in getTimeList('minutes')" :key="minutes">{{minutes}}</option>
            </select>
          </td>
        </tr>
        <!-- <tr>
          <td>Centro comercial Moctezuma</td>
          <td>Francisco Chang</td>
          <td>Mexico</td>
        </tr> -->
      </table>
    </div>
    <div class="condition">
      <div>
        <h3>Condition</h3>
      </div>
      <table>
        <tr>
          <td>Subject Sensor:</td>
          <td>
            <select class="size" @change="onChangeSensorType($event)">
            <option value="" selected disabled hidden>sensor type</option>
            <option v-for="type in sensorType" :key="type">{{type}}</option>
          </select>
          </td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>sensor id</option>
              <option v-for="sensorId in sensorIds" :key="sensorId">{{sensorId}}</option>
            </select>
          </td>
        </tr>
        <tr>
          <td>Time:</td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>hours</option>
              <option v-for="hour in getTimeList('hours')" :key="hour">{{hour}}</option>
            </select>
          </td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>minutes</option>
              <option v-for="minutes in getTimeList('minutes')" :key="minutes">{{minutes}}</option>
            </select>
          </td>
        </tr>
        <tr>
          <td>Recurring:</td>
          <td>
            <select class="size">
              <option>yes</option>
              <option>no</option>
            </select>
          </td>
        </tr>
        <tr>
          <td>Reading:</td>
          <td>
            <select class="size">
              <option value="" selected disabled hidden>relation</option>
              <option>greater than</option>
              <option>less than</option>
              <option>equans to</option>
            </select>
          </td>
          <td>
            <input class="size" placeholder="0"/>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import {sensor} from "@/store/sensor-type"
import {getAllLatest} from '@/services/sensorService.js'
import { getActuatorByType } from '@/services/actuatorService.js';

export default {
  name: "ActuatorSetting",
  data() {
    return {
      hours: [],
      minutes: [],
      sensorType: [],
      selectedSensorType: "",
      selectedActuatorType: "",
      sensorIds: [],
      actuatorIds: []
    }
  },
  methods: {
    getTimeList(option) {
      let length = 0

      if (option === "hours") {
        length = 24
      }
      else if (option === "minutes") {
        length = 60
      }
      let timePeriod = []

      for (let t in Array.from(Array(length).keys())) {
        let time = (t < 10 ? "0" : "") + t
        timePeriod.push(time)
      }
      return timePeriod
    },
    getIntensity() {
      let percentage = []

      for (let p in Array.from(Array(10).keys())) {
        p = (parseInt(p) + 1) * 10
        percentage.push(p + "%")
      }

      return percentage
    },
    onChangeSensorType(event) {
      this.selectedSensorType = event.target.value
      this.getSensorIds()
    },
    onChangeActuatorType(event) {
      this.selectedActuatorType = event.target.value
      this.getActuatorIds()
    },
    async getSensorIds() {
      const response = await getAllLatest()

      if (response.status !== 200) {
        this.sensorIds = []
        return
      }
      let sensorIds = []
      const sensorList = response.data.data

      for (let sensor of sensorList.values()) {
        if (sensor["sensor_type"] == this.selectedSensorType) {
          sensorIds.push(sensor["sensor_id"])
        }
      }
      this.sensorIds = sensorIds
    },
    async getActuatorIds() {
      const response = await getActuatorByType("sprinkler")
      console.log(response)

      if (response.status !== 200) {
        this.actuatorIds = []
        return
      }

      let actuatorIds = []
      const actuatorList = response.data.data

      for (let actuator of actuatorList.values()) {
        if (actuator["sensor_type"] == this.selectedActuatorType) {
          actuatorIds.push(actuator["sensor_id"])
        }
      }
      this.actuatorIds = actuatorIds
    }
  },
  async created() {
    this.sensorType = sensor.value.types
  }
}

</script>

<style scoped>

.instruction {
  padding-top: 10px;
  padding-bottom: 40px;
}

.containter {
  padding-bottom: 35px;
}

.option {
  display: flex;
  align-items: center;
  padding-top: 20px;
}

.size{
  width: 8vw;
  height: 2vw;
}

td {
  padding-top: 15px;
  padding-left: 30px;
}

tr {
  padding-left: 30px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 90px;
  height: 34px;
}

.switch input {display:none;}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ca2222;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2ab934;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(55px);
  -ms-transform: translateX(55px);
  transform: translateX(55px);
}

.on
{
  display: none;
}

.on, .off
{
  color: white;
  position: absolute;
  transform: translate(-50%,-50%);
  top: 50%;
  left: 50%;
  font-size: 10px;
  font-family: Verdana, sans-serif;
}

input:checked+ .slider .on
{display: block;}

input:checked + .slider .off
{display: none;}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;}
</style>