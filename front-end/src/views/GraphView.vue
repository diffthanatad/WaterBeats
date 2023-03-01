<template>
  <div class="container">
    <h1>Visualisation Page</h1>
    <hr>
    <div>
      <LineChart />
    </div>
    <hr>
    <div class="map" style="width:87%;height:50%">
      <MapComp :inputDevices="devices" />
    </div>
    <div class="space"></div>
  </div>
</template>

<style scoped>

h1 {
  text-align: center;
  padding-top: 30px;
}
.map {
  padding-left: 20px;
}
.space {
  padding-top:420px
}
</style>

<script>
import LineChart from '@/components/LineChart.vue'
import MapComp from '@/components/Map/MapComp.vue'

export default {
  name: 'GraphView',
  components: {
    LineChart,
    MapComp
  },
  data () {
    return {
      devices: [
          {
              id: "5",
              type: "Water Sprinkler",
              status: "watering",
              location: [51.52397881654594, -0.130105538694122]
          },
          {
              id: "6",
              type: "Water Sprinkler",
              status: "off",
              location: [51.52329792648238, -0.13508371862180735]
          }
      ],
      rules: {
          temperatureLow: "1",
          temperatureHigh: "2",
          soilMoistureLow: "3",
          soilMoistureHigh: "4",
          minute: "10",
          time: "10:00",
      },
    }
  },
  methods: {
  }
}
</script>
