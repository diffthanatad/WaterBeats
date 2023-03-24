<template>
  <div class="container">
    <h1>Visualisation Page</h1>
    <hr>
    <div>
      <LineChart />
    </div>
    <hr>
    <div class="map" style="width:87%;height:50%">
      <MapComp />
    </div>
    <div class="space"></div>
  </div>
</template>

<script>
import LineChart from '@/components/Charts/LineChart.vue'
import MapComp from '@/components/Map/MapComp.vue'
import { getLatestReadingForAllDevices } from "@/services/deviceService.js";
import moment from 'moment';

export default {
  name: 'GraphView',
  components: {
    LineChart,
    MapComp,
  },
  data() {
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
  mounted() {
    this.getAllDevices()
  },
  methods: {
    async getAllDevices() {
      try {
        const response = await getLatestReadingForAllDevices();

        if (response.status === 200) {
          var DEVICES = response.data.data;

          DEVICES.forEach(element => {
            element.timestamp = moment(element.time).format('Do MMMM YYYY, h:mm:ss a');
            var temp = Number(element.data);
            if (temp) { element.value = `${temp.toFixed(2)} ${element.unit}`; }
            else { element.value = "" }
          });

          this.$store.dispatch("device/update", DEVICES);
        }
      } catch (error) {
        console.log("HomeView.vue, getAllDevices():", error);
      }
    },
  }
}
</script>

<style scoped>
h1 {
  text-align: center;
  padding-top: 30px;
}

.map {
  margin-left: auto;
  margin-right: auto;
}

.space {
  padding-top: 420px
}
</style>