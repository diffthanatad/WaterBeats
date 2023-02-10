<template>
  <div class="home">
    <MapComp :inputDevices="devices" />
  </div>
</template>

<script>
import MapComp from '@/components/Map/MapComp.vue'
import { getLatestReadingForAllDevices } from "@/services/deviceService.js";

export default {
  name: 'HomeView',
  components: {
    MapComp,
  },
  data() {
    return {
      devices: [
        {
          id: "1",
          type: "Soil Moisture Sensor",
          status: "on",
          value: "0.55 wfv",
          timestamp: "2023-01-04 18:51:04",
          location: [51.524692684598826, -0.13405083079203617]
        },
        {
          id: "2",
          type: "Soil Moisture Sensor",
          status: "off",
          value: null,
          timestamp: null,
          location: [51.524926705352485, -0.13249806913374523]
        },
        {
          id: "3",
          type: "Temperature Sensor",
          status: "on",
          value: "11°C",
          timestamp: "2023-01-04 16:30:22",
          location: [51.52191552403864, -0.13179715055845592]
        },
        {
          id: "4",
          type: "Temperature Sensor",
          status: "on",
          value: "12°C",
          timestamp: "2023-01-04 15:09:22",
          location: [51.52597470028996, -0.13253025564190157]
        },
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
        },
        {
          id: "9",
          type: "dddWater Sprinkler",
          status: "off",
          location: [51.52306410413633, -0.12788555112319272]
        }
      ],
    };
  },
  mounted() {
    // this.getAllDevices();
  },
  methods: {
    async getAllDevices() {
      try {
        const response = await getLatestReadingForAllDevices();

        if (response.status !== 200) { return; }

        this.devices = response.data;
      } catch (error) {
        console.log("HomeView.vue, getAllDevices():", error);
      }

    }
  },
}
</script>
