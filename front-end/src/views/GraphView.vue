<template>
  <div class="container">
    <!-- <div class="sensor-info"> -->
      <!-- <SensorList /> -->
    <!-- </div> -->
    <div class="chart" style="width:60%;">
      <LineChart />
    </div>
    <div class="sensors-list">
      <SensorList />
    </div>
  </div>
</template>

<style scoped>
/* div {
  margin-left: auto;
  margin-right: auto;
} */
.container {
  overflow: hidden;
  padding-top: 50px;
}

.chart {
  float: left;
  padding-top: 50px;
}

.sensors-list {
  overflow: hidden;
  padding-left: 80px;
  padding-top: 50px;
}
.sensor-info {
  float: left;
  padding-right: 80px;
  padding-top: 50px;
}
</style>

<script>
import LineChart from '@/components/LineChart.vue'
import SensorList from '@/components/SensorList.vue'

export default {
  name: 'GraphView',
  components: {
    LineChart,
    SensorList
  },
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>
