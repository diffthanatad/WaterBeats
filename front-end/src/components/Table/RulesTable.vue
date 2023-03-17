<template>
  <table>
    <tr>
      <th>Actuator ID</th>
      <th>State</th>
      <th>Intensity</th>
      <th>Duration (Min)</th>
      <th>Subject Sensor</th>
      <th>Condition</th>
      <th></th>
    </tr>
    <tr v-for="rule in rulesList" :key="rule['actuator_id']">
      <td>{{rule["actuator_id"]}}</td>
      <td>{{rule["actuator_state"]}}</td>
      <td>{{rule["intensity"]}}%</td>
      <td>{{rule["duration"]}}</td>
      <td>{{rule["subject_sensor"]}}</td>
      <td>{{rule["condition"]}}</td>
      <td @click="deleteRule(rule['actuator_id'])">
        <button type="button" class="btn btn-danger">
          <i class="bi bi-trash"></i>
        </button>
      </td>
    </tr>
  </table>
</template>

<script>
import store from "@/store"
import { getAllRules, deleteRuleByActuatorId } from '@/services/ruleService'

export default {
  name: 'RulesTable',
  store,
  data() {
    return {
      rulesList: []
    }
  },
  methods: {
    async updateRulesList() {
      const response = await getAllRules()

      const rules = response.data.data
      let rulesList = []

      for (const i in rules) {
        rules[i]['actuator_state'] = rules[i]['actuator_state'] ? 'ON' : 'OFF'

        const reading = parseFloat(rules[i]['sensor_reading'])
        rules[i]['sensor_reading'] = (reading % 1 != 0) ? reading : parseInt(reading)
        rules[i]['condition'] = rules[i]['relation'] + " " + rules[i]['sensor_reading']

        rulesList.push(rules[i])
      }

      this.rulesList = rulesList
    },
    async deleteRule(actuatorId) {
      const answer = confirm("Are you sure you want to delete this rule?")

      if (!answer) {
        return
      }
      const response = await deleteRuleByActuatorId(actuatorId)

      if (response.status !== 200) {
        return
      }
      this.updateRulesList()
    }
  },
  created() {
    this.updateRulesList()
  }
}
</script>

<style scoped>

table {
  border-spacing: 0;
  width: 100%;
  border: None;
}

th, td {
  padding: 11px;
}

tr {
  border-bottom: 1px solid #ddd;
}
tr:nth-child(even) {
  background-color: #f2f2f2
}

td {
  color: #495057;
  text-align: center;
  font-size: 13px;
}

th {
  text-align: left;
  font-size: 13px;
}

</style>