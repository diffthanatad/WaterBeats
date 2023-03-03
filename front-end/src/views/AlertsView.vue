<template>
  <div>
    <h1>ALERTS</h1>
    <AlertsConfig />
  </div>
</template>

<script>
import AlertsConfig from '@/components/AlertsConfig.vue'

export default {
  name: 'AlertsView',
  components: { AlertsConfig },
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
  padding-top: 30px;
  padding-bottom: 70px;
}
</style>