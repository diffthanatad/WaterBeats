import { getAllLatest, getLatestById, getRecord } from '@/services/sensorService'


const getDefaultState = () => {
  return {
    currentSensorId: "",
    currentSensorData: "",
    currentSensorUnit: "",
    currentSensorLocation: "",
    selectedSensorType: "temperature",
    lastestTimestamp: "",
    sensorIdList: [],
    selectedSensorIdList: [],
    chartData: {
      labels: [],
      datasets: []
    },
    sensorTypeNames: ["temperature", "soil_moisture", "water_level", "water_pollution"]
  }
}
const state = getDefaultState();

const mutations = {
    RESET_STATE(state) {
        Object.assign(state, getDefaultState());
    },
    RESET_SENSOR_LIST(state) {
        state.currentSensorId = ""
        state.currentSensorData = ""
        state.currentSensorUnit = ""
        state.currentSensorLocation = ""
    },
    setSensorId(state, sensorId) {
        state.currentSensorId = sensorId
    },
    setSensorData(state, sensorData) {
        state.currentSensorData = sensorData
    },
    setSensorUnit(state, sensorUnit) {
        state.currentSensorUnit = sensorUnit
    },
    setSensorLocation(state, sensorLocation) {
        state.currentSensorLocation = sensorLocation
    },
    setSensorType(state, sensorType) {
        state.selectedSensorType  = sensorType
    },
    setTimestamp(state, timestamp) {
        state.lastestTimestamp = timestamp
    },
    setSensorIdList(state, sensorIdList) {
        state.sensorIdList = sensorIdList
    },
    setSelectedSensorIdList(state, selectedSensorIdList) {
        state.selectedSensorIdList = selectedSensorIdList
    },
    setChartData(state, chartData) {
        state.chartData = chartData
    }
};

const actions = {
    async updateSensorInfo({ commit, state }) {
        const response = await getLatestById(state.currentSensorId)

        if (response.status !== 200) {
            commit('RESET_STATE')
            return
        }
        const sensorInfo = response.data.data

        commit('setSensorData', sensorInfo.data.toFixed(2))
        commit('setSensorUnit', sensorInfo.unit)
        commit('setSensorLocation', sensorInfo.location)
        commit('setTimestamp', response.data.data.time)
    },
    async updateSensorIdList({ commit, state }) {
        const response = await getAllLatest()

        if (response.status !== 200) {
            commit('RESET_STATE')
            return
        }

        let sensorIdList = []
        const sensorList = response.data.data

        for (const sensor of sensorList.values()) {
          if (sensor["type"] == state.selectedSensorType) {
            sensorIdList.push(sensor["id"])
          }
        }
        commit('setSensorId', sensorIdList[0])
        commit('setSensorIdList', sensorIdList)
    },
    async updateChartDataMultiple({ state, commit, dispatch }) {
        await dispatch('updateSensorInfo')

        let date = new Date(state.lastestTimestamp)
        let end = date.toISOString()

        date.setDate(date.getDate() - 365)
        let start = date.toISOString()

        let timestampList = []
        let datasets = []

        for (const [i, sensorId] of state.selectedSensorIdList.entries()) {
            const response = await getRecord(sensorId, start, end)

            if (response.status !== 200) {
                commit('RESET_STATE')
                return
            }
            const sensor = response.data.data.slice(0, 100);
            const sensorData = { label: sensorId, data: [] }

            for (const data of sensor) {
                if (i === 0) {
                    let date = new Date(data["time"])

                    let hour = date.getHours()
                    hour = (hour < 10) ? "0" + hour : hour

                    let minute = date.getMinutes()
                    minute = (minute < 10) ? "0" + minute : minute

                    timestampList.push(date.toLocaleDateString() + " " + hour + ":" + minute)
                }
                sensorData['data'].push(data['data'])
            }
            datasets.push(sensorData)
        }
        commit('setChartData', {
            labels: timestampList,
            datasets: datasets
        })
    },
    async updateChartData ({ commit, state, dispatch }) {
        await dispatch('updateSensorInfo')

        let date = new Date(state.lastestTimestamp)
        let end = date.toISOString()

        date.setDate(date.getDate() - 365)
        let start = date.toISOString()

        const response = await getRecord(state.currentSensorId, start, end)

        if (response.status !== 200) {
            commit('RESET_STATE')
            return
        }
        const sensor = response.data.data.slice(0, 100);
        let timestampList = []
        let sensorDataList = []

        for (const data of sensor) {
            let date = new Date(data["time"])

            let hour = date.getHours()
            hour = (hour < 10) ? "0" + hour : hour

            let minute = date.getMinutes()
            minute = (minute < 10) ? "0" + minute : minute

            timestampList.push(date.toLocaleDateString() + " " + hour + ":" + minute)
            sensorDataList.push(data["data"])
        }

        commit('setChartData', {
            labels: timestampList,
            datasets: [{
                label: state.currentSensorId,
                data: sensorDataList
            }],
        })
    }
};

export default {
    namespaced: true,
    state,
    mutations,
    actions
}
