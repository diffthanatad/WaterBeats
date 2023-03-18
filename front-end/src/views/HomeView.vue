<template>
  <div class="home">
    <MapComp />
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
      sendAPIQueryInterval: null,
    };
  },
  mounted() {
    this.getAllDevices()
    this.repeatTheAPICall()
    this.$store.dispatch("device/start");
  },
  computed: {
    keepCallAPI() {
      return this.$store.getters['device/getAutomatic'];
    }
  },
  methods: {
    repeatTheAPICall() {
      try {
        this.sendAPIQueryInterval = setInterval(async () => await this.getAllDevices(), 5000);
      } catch (error) {
        console.log("HomeView.vue, repeatTheAPICall():", error);
      }
    },
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
    stopRecurrentAPICall() {
      clearInterval(this.sendAPIQueryInterval);
    }
  },
  watch: {
    keepCallAPI(newValue) {
      if (newValue === false) {
        this.stopRecurrentAPICall();
      }
    }
  }
}
</script>
