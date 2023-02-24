<template>
  <TabsGraph @click="updateLineGraph"/>
  <Line
    id="my-chart-id"
    :options="chartOptions"
    :data="chartData"
  />
</template>

<style scoped>
</style>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement} from 'chart.js'
import TabsGraph from '@/components/TabsGraph.vue'
import {tabSelect} from "@/store/tab-select.js"
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
  components: { Line, TabsGraph },
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
            }
          }
        }
      }
    }
  },
  methods: {
    updateLineGraph() {
      let selectedTab = tabSelect.value.selectedTab
      let labels = chart.value.timestamp
      let chartData = chart.value.sensorData[selectedTab]


      this.chartData = {
        labels: labels,
        datasets: [{data: chartData}]
      }
    }
  },
  created() {
    this.updateLineGraph()
  }
}
</script>