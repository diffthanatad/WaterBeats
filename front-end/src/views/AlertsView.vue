<template>
  <div>
    <h1>ALERTS</h1>
    <FormAlertSetting />
    <br>
    <AlertsTable />
  </div>
</template>

<script>
import AlertsTable from '@/components/Table/AlertsTable.vue'
import FormAlertSetting from '@/components/Form/FormAlertSetting.vue'

export default {
  name: 'AlertsView',
  components: { FormAlertSetting, AlertsTable },
  data() {
    return {}
  },
  methods: {
  }
}

</script>

<style scoped>
h1 {
  text-align: center;
  padding-top: 50px;
  padding-bottom: 50px;
}
</style>