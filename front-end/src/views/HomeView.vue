<template>
  <div class="home">
    <MapComp :inputDevices="devices" />
  </div>
</template>

<script>
import moment from 'moment';
import MapComp from '@/components/Map/MapComp.vue'
import { getLatestReadingForAllDevices } from "@/services/deviceService.js";

export default {
  name: 'HomeView',
  components: {
    MapComp,
  },
  data() {
    return {
      devices: [],
    };
  },
  mounted() {
    this.getAllDevices();
  },
  methods: {
    async getAllDevices() {
      try {
        const response = await getLatestReadingForAllDevices();

        if (response.status === 200) {
          var DEVICES = response.data.data;
          
          DEVICES.forEach(element => {
            element.timestamp = moment(element.time).format('MMMM Do YYYY, h:mm:ss a');
            var temp = Number(element.data);
            if (temp) { element.value = `${temp.toFixed(2)} ${element.unit}`; } 
            else { element.value = "" }
          });

          this.$store.dispatch("device/update", DEVICES);
        }
      } catch (error) {
        console.log("HomeView.vue, getAllDevices():", error);
      }

    }
  },
}
</script>
