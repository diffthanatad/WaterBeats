<template>
  <div class="containter">
    <div class="events">
      <form @submit.prevent="onSubmitRule" id="rule-setting">
        <div class="headers">
          <h4 id="header-condition">Condition: </h4>
          <div class="missingFields" v-if="isMissingFieldCondition">
            {{ errorMessageCondition }}
          </div>
        </div>
        <table class="events-table">
          <tr>
            <td class="first-column">Subject Sensor</td>
            <td>
              <select class="size dropdown" id="subject-sensor" @change="onChangeSensorType($event)">
                <option value="0" selected disabled>sensor type</option>
                <option v-for="type in sensorType" :key="type">{{type}}</option>
              </select>
            </td>
            <td>
              <select class="size dropdown" id="sensor-id" name="sensor_id">
                <option value="0" selected disabled>sensor id</option>
                <option v-for="sensorId in sensorIds" :key="sensorId">{{sensorId}}</option>
              </select>
            </td>
            <td class="td-width"></td>
          </tr>
          <tr>
            <td>Trigger when reading</td>
            <td>
              <select class="size dropdown" id="relation" name="relation">
                <option value="0" selected disabled>relation</option>
                <option>&gt;</option>
                <option>&lt;</option>
                <option>&gt;=</option>
                <option>&lt;=</option>
                <option>==</option>
              </select>
            </td>
            <td>
              <input class="size" id="sensor-reading" name="reading" placeholder="0"/>
            </td>
            <td></td>
          </tr>
        </table>
        <br>
        <div class="headers">
          <h4 id="header-task">Task:</h4>
          <div class="missingFields" v-if="isMissingFieldTask">
            {{ errorMessageTask }}
          </div>
        </div>
        <table class="events-table">
          <tr>
            <td class="first-column">Target Actuator</td>
            <td>
              <select class="size dropdown" id="actuator-type" @change="onChangeActuatorType($event)" name="actuator_type">
                <option value="0" selected disabled>actuator type</option>
                <option>sprinkler</option>
                <option>pump</option>
              </select>
            </td>
            <td>
              <select class="size dropdown" id="actuator-id" name="actuator_id">
                <option value="0" selected disabled>actuator id</option>
                <option v-for="actuatorId in actuatorIds" :key="actuatorId">{{actuatorId}}</option>
              </select>
            </td>
            <td class="td-width"></td>
          </tr>
          <tr>
            <td>Actuator State</td>
            <td>
              <label class="switch">
                <input type="checkbox" id="actuator-state" name="actuator_state">
                <div class="slider round">
                  <span class="on">ON</span>
                  <span class="off">OFF</span>
                </div>
              </label>
            </td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>Intensity</td>
            <td>
              <select class="size dropdown" id="intensity" name="intensity">
                <option value="0" selected disabled>percentage</option>
                <option v-for="percentage in getIntensity()" :key="percentage">{{percentage}}</option>
              </select>
            </td>
            <td></td>
            <td></td>
          </tr>
          <tr>
            <td>Duration</td>
            <td>
              <select class="size dropdown" id="hours" name="hours">
                <option value="0" selected disabled>hours</option>
                <option v-for="hour in getTimeList('hours')" :key="hour">{{hour}}</option>
              </select>
            </td>
            <td>
              <select class="size dropdown" id="minutes" name="minutes">
                <option value="0" selected disabled>minutes</option>
                <option v-for="minutes in getTimeList('minutes')" :key="minutes">{{minutes}}</option>
              </select>
            </td>
            <td></td>
          </tr>
        </table>
        <br>
        <div class="btn-save row justify-content-center">
          <button class="btn btn-primary"><i class="bi bi-save2"></i>Save</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import store from "@/store"
import { mapState } from 'vuex';
import {getAllLatest} from '@/services/sensorService.js'
import { getActuatorByType } from '@/services/actuatorService.js';
import { addRule, getRuleByActuatorId, updateRuleByActuatorId } from '@/services/ruleService.js';

export default {
  name: "RulesConfig",
  store,
  data() {
    return {
      sensorType: [],
      sensorIds: [],
      actuatorIds: [],
      isMissingFieldCondition: false,
      isMissingFieldTask: false,
      errorMessageCondition: "",
      errorMessageTask: ""
    }
  },
  methods: {
    getTimeList(option) {
      let length = 0

      if (option === "hours") {
        length = 26
      }
      else if (option === "minutes") {
        length = 61
      }
      let timePeriod = []

      for (let t in Array.from(Array(length - 1).keys())) {
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
      this.getSensorIds(event.target.value)
    },
    onChangeActuatorType(event) {
      this.getActuatorIds(event.target.value)
    },
    async addRule(subject_sensor, sensor_reading, relation, actuator_id,
      actuator_type, actuator_state, intensity, duration) {

      const response = await addRule(
        subject_sensor,
        sensor_reading,
        relation,
        actuator_id,
        actuator_type,
        actuator_state,
        intensity,
        duration
      )
      if (response.status !== 200) {
        return
      }
    },
    async updateRule(subject_sensor, sensor_reading, relation, actuator_id,
      actuator_state, intensity, duration) {

      const response = await updateRuleByActuatorId(
        subject_sensor,
        sensor_reading,
        relation,
        actuator_id,
        actuator_state,
        intensity,
        duration
      )
      if (response.status !== 200) {
        return
      }
    },
    async onSubmitRule(event) {

      const hours = parseInt(event.target.elements.hours.value)
      const minutes = parseInt(event.target.elements.minutes.value)
      const total_duration_in_minutes = (hours * 60) + minutes

      const subject_sensor = event.target.elements.sensor_id.value
      const sensor_reading = event.target.elements.reading.value ? event.target.elements.reading.value : 0
      const relation = event.target.elements.relation.value
      const actuator_id = event.target.elements.actuator_id.value
      const actuator_type = event.target.elements.actuator_type.value
      const actuator_state = event.target.elements.actuator_state.checked ? 1 : 0
      const intensity = event.target.elements.intensity.value.replace("%", "")
      const duration = total_duration_in_minutes

      if (this.isMissingFields(subject_sensor, relation, actuator_id, intensity, hours, minutes)) {
        return
      }
      const response = await getRuleByActuatorId(actuator_id)

      if (response.data.data == null || response.data.data.length === 0) {
        await this.addRule(
          subject_sensor, sensor_reading, relation, actuator_id,
          actuator_type, actuator_state, intensity, duration
        )
      }
      else {
        await this.updateRule(
          subject_sensor, sensor_reading, relation, actuator_id,
          actuator_state, intensity, duration
        )
      }
      this.resetForm()
    },
    isMissingFields(subject_sensor, relation, actuator_id, intensity, hours, minutes) {
      let missingFieldCondition = ""
      let missingFieldTask = ""

      let isMissingFieldCondition = false
      let isMissingFieldTask = false

      if (relation == 0) {
        missingFieldCondition = "Relation"
        isMissingFieldCondition = true

        const element = document.querySelector('#relation');
        element.style.borderColor = 'red';
      }
      if (subject_sensor == 0) {
        missingFieldCondition = "Subject Sensor"
        isMissingFieldCondition = true

        const element1 = document.querySelector('#subject-sensor');
        element1.style.borderColor = 'red';

        const element2 = document.querySelector('#sensor-id');
        element2.style.borderColor = 'red';
      }

      if ((hours == 0 && minutes == 0)) {
        missingFieldTask = "Duration"
        isMissingFieldTask = true

        const element1 = document.querySelector('#hours');
        element1.style.borderColor = 'red';

        const element2 = document.querySelector('#minutes');
        element2.style.borderColor = 'red';
      }
      if (intensity == 0) {
        missingFieldTask = "Intensity"
        isMissingFieldTask = true

        const element = document.querySelector('#intensity');
        element.style.borderColor = 'red';
      }
      if (actuator_id == 0) {
        missingFieldTask = "Target Actuator"
        isMissingFieldTask = true

        const element1 = document.querySelector('#actuator-type');
        element1.style.borderColor = 'red';

        const element2 = document.querySelector('#actuator-id');
        element2.style.borderColor = 'red';
      }

      if (isMissingFieldCondition) {
        this.isMissingFieldCondition = true
        this.errorMessageCondition = `Error: '${missingFieldCondition}' is a required field.`
      }
      if (isMissingFieldTask) {
        this.isMissingFieldTask = true
        this.errorMessageTask = `Error: '${missingFieldTask}' is a required field.`
      }

      return isMissingFieldCondition || isMissingFieldTask
    },
    resetForm() {
      document.getElementById('subject-sensor').value = "0";
      document.getElementById('sensor-id').value = "0";
      document.getElementById('relation').value = "0";
      document.getElementById('sensor-reading').value = "0";
      document.getElementById('actuator-id').value = "0";
      document.getElementById('actuator-type').value = "0";
      document.getElementById('actuator-state').checked = false;
      document.getElementById('intensity').value = "0";
      document.getElementById('hours').value = "0";
      document.getElementById('minutes').value = "0";

      this.isMissingFieldCondition = false
      this.isMissingFieldTask = false

      let element = document.querySelector('#subject-sensor');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#sensor-id');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#relation');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#sensor-reading');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#actuator-id');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#actuator-type');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#intensity');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#hours');
      element.style.borderColor = '#6c757d';

      element = document.querySelector('#minutes');
      element.style.borderColor = '#6c757d';
    },
    async getSensorIds(sensorType) {
      const response = await getAllLatest()

      if (response.status !== 200) {
        this.sensorIds = []
        return
      }
      let sensorIds = []
      const sensorList = response.data.data

      for (let sensor of sensorList.values()) {
        if (sensor["type"] === sensorType) {
          sensorIds.push(sensor["id"])
        }
      }
      this.sensorIds = sensorIds
    },
    async getActuatorIds(actuatorType) {
      const response = await getActuatorByType(actuatorType)

      if (response.status !== 200) {
        this.actuatorIds = []
        return
      }

      let actuatorIds = []
      const actuatorList = response.data.data

      for (let actuator of actuatorList.values()) {
        actuatorIds.push(actuator["id"])
      }
      this.actuatorIds = actuatorIds
    }
  },
  computed: mapState({
    sensorTypeNames: state => state.sensors.sensorTypeNames
  }),
  async created() {
    this.sensorType = this.sensorTypeNames
  }
}

</script>

<style scoped>
#header-condition {
  padding-bottom: 10px;
  padding-right: 60px;
}

#header-task {
  padding-top: 5px;
  padding-bottom: 10px;
  padding-right: 112px;
}

#sensor-reading {
  text-align: center;
  color: #6c757d;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.bi {
    margin-right: 5px;
}

.btn {
    width: 100px;
}

.btn-save {
  padding-top: 10px;
}

.containter {
  padding-bottom: 35px;
}

.dropdown {
  color: #6c757d;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.events {
  /* padding-top: 10px; */
  padding-bottom: 10px;
  width: -webkit-max-content;
  width: -moz-max-content;
  width: max-content;
}

.first-column {
  width: 175px;
}

.headers {
  display: flex;
  align-items: center;
}

.missingFields {
  color: #F80000;
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

.option {
  display: flex;
  align-items: center;
  padding-top: 20px;
}

.size{
  width: 110px;
  height: 30px;
}

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

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;}

.switch {
  position: relative;
  display: inline-block;
  width: 90px;
  height: 34px;
}

.switch input {display:none;}

.td-width {
  width: 175px;
}

input:checked + .slider {
  background-color: #2ab934;
}

input:checked + .slider:before {
  -webkit-transform: translateX(55px);
  -ms-transform: translateX(55px);
  transform: translateX(55px);
}

input:checked+ .slider .on
{display: block;}

input:checked + .slider .off
{display: none;}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

select {
  text-align: center;
}

table {
  border-spacing: 0;
  border: 1px solid #ddd;
  width: 100%;
  font-size: 14px;
}

td, th {
  text-align: left;
  padding: 10px;
  border-width: 1px;
  border-top: transparent;
  border-bottom: transparent;
  border-left: #ddd;
  border-right: #ddd;
}

tr {
  background-color: #f2f2f2
}

</style>