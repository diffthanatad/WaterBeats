<template>
  <div class="alert-list container">
    <table class="table table-hover table-sm">
      <tr>
        <th>Sensor ID</th>
        <th>Sensor Type</th>
        <th>Threshold</th>
        <th>Relation</th>
        <th>Created At</th>
        <th>Updated At</th>
        <th></th>
      </tr>
      <tr v-for="alert in alertList" :key="alert['sensor_id']">
        <td>{{ alert['sensor_id'] }}</td>
        <td>{{ alert['sensor_type'] }}</td>
        <td>{{ alert['threshold'] }}</td>
        <td>{{ alert['relation'] }}</td>
        <td>{{ getDate(alert['created_at']) }}</td>
        <td>{{ getDate(alert['updated_at']) }}</td>
        <td @click="deleteAlertList(alert['sensor_id'])">
          <button type="button" class="btn btn-danger">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      </tr>
    </table>
    <confirm-dialogue ref="confirmDialogue"></confirm-dialogue>
  </div>
</template>

<script>
import { deleteAlertBySensorId } from '@/services/alertService'
import ConfirmDialogue from "@/components/Modal/ConfirmDialogue.vue";
import { mapState } from 'vuex';
import store from "@/store"


export default {
  name: "AlertsTable",
  store,
  components: {
    ConfirmDialogue
  },
  data() {
    return {
    }
  },
  computed: mapState({
    alertList: state => state.alerts.alertList
  }),
  methods: {
    async deleteAlertList(sensorId) {
      const ok = await this.$refs.confirmDialogue.show({
        title: 'Delete Alert',
        message: 'Do you want to delete this alert?',
        okButton: 'yes',
      });

      if (!ok) {
        return
      }
      const response = await deleteAlertBySensorId(sensorId)

      if (response.status != 200) {
        return
      }
      await store.dispatch('alerts/updateAlertList')
    },
    getDate(timestamp) {
      return new Date(timestamp).toLocaleString()
    }
  },
  async created() {
    await store.dispatch('alerts/updateAlertList')
  }
}
</script>

<style scoped>

.alert-list {
  padding-top: 50px;
}

.btn {
  background-color: #dd3445;
  width: 35px;
  height: 35px
}

.btn:hover {
  background-color: #bb2c3b
}

tr {
  border-bottom: 1px solid #e0e4e4;
}

td, th {
  padding-top: 5px;
  padding-bottom: 7px;
}

</style>