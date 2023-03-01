<template>
  <div class="container">
    <div class="sensor-info">
      <SensorInfo ref="sensorInfo" />
    </div>
    <div class="chart" style="width:60%;">
      <TabsGraph @click="updateSensorList()"/>
      <Line
        id="my-chart-id"
        :options="chartOptions"
        :data="chartData"
      />
    </div>
    <div class="sensor-list">
      <SensorList ref="sensorList" :updateLineGraph="updateLineGraph" :updateSensorInfo="updateSensorInfo"/>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  padding-top: 10px;
}

.sensor-info {
  padding-top: 100px;
}

.chart {
  padding-top: 50px;
}

.sensor-list {
  padding-left: 50px;
  padding-top: 50px;
}
</style>

<script setup>
import SensorList from '@/components/SensorList.vue'
import SensorInfo from '@/components/SensorInfo.vue'
import { ref } from 'vue'

const sensorList = ref(null)
const sensorInfo = ref(null)

function updateSensorList() {
  sensorList.value?.childMethod()
}

function updateSensorInfo() {
  sensorInfo.value?.childMethod()
}

</script>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement} from 'chart.js'
import TabsGraph from '@/components/TabsGraph.vue'
import {getRecord} from '@/services/sensorService.js'
// import {tabSelect} from "@/store/tab-select.js"
import {chart} from "@/store/chart-data.js"

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'LineChart',
  components: { Line, TabsGraph, SensorList, SensorInfo },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: []
      },
      chartOptions: {
        responsive: true,
        backgroundColor: 'rgb(255, 99, 132)',
        color: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y:{
            title: {
              display: true,
              text: "Celsius°"
            }
          },
          x: {
            title: {
              display:true,
              text: "TIME"
            },
            ticks: {
              maxRotation: 50,
              minRotation: 50
            }
          }
        }
      }
    }
  },
  methods: {
    async updateLineGraph() {
      let sensorId = chart.value.sensorId

      const date = new Date()
      let end = date.toISOString()

      date.setDate(date.getDate() - 1);
      let start = date.toISOString()

      const response = await getRecord(sensorId, start, end)

      if (response.status !== 200 || sensorId === "") {
        this.chartData = {
          labels: [],
          datasets: [{data: []}]
        }
        return
      }
      const dataList = response.data.data
      let timestamps = []
      let sensorData = []

      for (let data of dataList) {
        let date = new Date(data["time"])
        let hour = date.getHours()
        let minute = date.getMinutes()

        timestamps.push(hour + ":" + minute)
        sensorData.push(data["data"])
      }

      this.chartData = {
        labels: timestamps,
        datasets: [{data: sensorData}]
      }
    }
  }
}
</script>