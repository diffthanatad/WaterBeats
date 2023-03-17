<template>
  <div class="container">
    <div class="sensor-info">
      <SensorInfo />
    </div>
    <div class="chart" style="width:60%;">
      <TabsGraph />
      <Line
        id="my-chart-id"
        :options="chartOptions"
        :data="chartData"
      />
    </div>
    <div class="sensor-list">
      <SensorList />
    </div>
  </div>
</template>


<script>
import { Line } from 'vue-chartjs'
import { mapState, mapActions } from 'vuex';
import SensorInfo from '@/components/Sensors/SensorInfo'
import SensorList from '@/components/Sensors/SensorList'
import TabsGraph from '@/components/Tabs/TabsGraph'
import store from "@/store"
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Colors} from 'chart.js'

ChartJS.register( CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Colors)

export default {
  name: 'LineChart',
  store,
  computed: mapState({
    chartData: state => state.sensors.chartData
  }),
  components: { Line, SensorInfo, SensorList, TabsGraph },
  data() {
    return {
      chartOptions: {
        responsive: true,
        pointStyle: false,
        borderWidth: 2.5,
        plugins: {
          legend: {
            display: true,
          },
          colors: {
            enabled: true,
            forceOverride: true
          }
        },
        scales: {
          y:{
            title: {
              // display: true,
              // text: "Celsius°"
            }
          },
          x: {
            title: {
              display:true,
              text: "TIMESTAMP"
            },
            ticks: {
              maxRotation: 70,
              minRotation: 0
            }
          }
        }
      }
    }
  },
  methods: mapActions('sensors', [
    'updateSensorIdList',
    'updateChartData'
  ]),
  async created() {
    await this.updateSensorIdList()
    await this.updateChartData()
  }
}
</script>


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
  padding-top: 30px;
}

.sensor-list {
  padding-left: 50px;
  padding-top: 50px;
}
</style>