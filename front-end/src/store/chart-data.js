import {ref} from "vue";

export const chart = ref({
    sensorId: "",
    timestamp: ["11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15",
                "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45"],
    sensorData: {
        "temperature": [22, 26, 28, 31, 28, 22, 22, 32, 26, 22, 21, 29, 25, 24, 33, 24, 31, 26, 31, 23],
        "moisture": [0.33, 0.32, 0.31, 0.30, 0.29, 0.28, 0.27, 0.30, 0.26, 0.25, 0.25, 0.25, 0.24, 0.24, 0.24, 0.23, 0.23, 0.23, 0.23, 0.22],
        "pollution_level": [16, 14, 14, 15, 14, 16, 16, 14, 15, 15, 14, 14, 15, 15, 15, 14, 15, 15, 15, 15],
        "water_level": [33, 23, 32, 27, 21, 29, 33, 27, 21, 25, 24, 29, 21, 32, 21, 29, 27, 29, 33, 24]
    },
    sensorIdList: {
        "temperature": [],
        "moisture": [],
        "pollution_level": [],
        "water_level": []
    },
    setSensorList(sensorType, sensorIds) {
        this.sensorIdList[sensorType] =  sensorIds
    },
    setSensorId(id) {
        this.sensorId = id
    }
});