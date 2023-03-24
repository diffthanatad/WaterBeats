<template>
  <div ref="refMapMarker" class="marker-component">
    <l-marker :lat-lng="marker.location">
      <l-icon :icon-size="dynamicSize" :icon-url="iconImage" />
      <l-popup style="width: 300px;">
        <div>
          <h5 style="text-align: center;"><i class="fas fa-tablet-alt"></i>{{ marker.type }}</h5>
          <div class="row">
            <div class="col-4"><i class="bi bi-person-badge"></i></div>
            <div class="col-8"> {{ marker.id ? marker.id : "N/A" }} </div>
          </div>
          <div class="row">
            <div class="col-4"><i class="bi bi-clock"></i></div>
            <div class="col-8"> {{ marker.timestamp }} </div>
          </div>
          <div class="row">
            <div class="col-4">Value</div>
            <div class="col-8"> {{ marker.value ? marker.value : "N/A" }}</div>
          </div>
          <div class="row">
            <div class="col-4"> Status: </div>
            <div class="col-8"> {{ marker.status ? marker.status : "N/A" }} </div>
          </div>
        </div>
      </l-popup>
    </l-marker>
  </div>
</template>

<script>
/* Import sensor icons: blue (i.e., on), black (i.e., off) and red (i.e., error). */
import icon_soil_moisture_blue from "@/assets/icon/icon_soil_moisture_blue.png";
import icon_soil_moisture_black from "@/assets/icon/icon_soil_moisture_black.png";
import icon_soil_moisture_red from "@/assets/icon/icon_soil_moisture_red.png";
import icon_temperature_blue from "@/assets/icon/icon_temperature_blue.png";
import icon_temperature_black from "@/assets/icon/icon_temperature_black.png";
import icon_temperature_red from "@/assets/icon/icon_temperature_red.png";
import icon_water_level_blue from "@/assets/icon/icon_water_level_blue.png";
import icon_water_level_black from "@/assets/icon/icon_water_level_black.png";
import icon_water_level_red from "@/assets/icon/icon_water_level_red.png";
import icon_water_pollution_blue from "@/assets/icon/icon_water_pollution_blue.png";
import icon_water_pollution_black from "@/assets/icon/icon_water_pollution_black.png";
import icon_water_pollution_red from "@/assets/icon/icon_water_pollution_red.png";
import icon_humidity_blue from "@/assets/icon/icon_humidity_blue.png";
import icon_humidity_black from "@/assets/icon/icon_humidity_black.png";
import icon_humidity_red from "@/assets/icon/icon_humidity_red.png";

/* Import actuator icons: blue (i.e., on), green (i.e., working), black (i.e., off) and red (i.e., error). */
import icon_sprinkler_blue from "@/assets/icon/icon_sprinkler_blue.png";
import icon_sprinkler_black from "@/assets/icon/icon_sprinkler_black.png";
import icon_sprinkler_green from "@/assets/icon/icon_sprinkler_green.png";
import icon_sprinkler_red from "@/assets/icon/icon_sprinkler_red.png";
import icon_pump_blue from "@/assets/icon/icon_pump_blue.png";
import icon_pump_black from "@/assets/icon/icon_pump_black.png";
import icon_pump_green from "@/assets/icon/icon_pump_green.png";
import icon_pump_red from "@/assets/icon/icon_pump_red.png";
import icon_motor_blue from "@/assets/icon/icon_motor_blue.png";
import icon_motor_black from "@/assets/icon/icon_motor_black.png";
import icon_motor_green from "@/assets/icon/icon_motor_green.png";
import icon_motor_red from "@/assets/icon/icon_motor_red.png";

import icon_questionMark_black from "@/assets/icon/icon_questionMark_black.png"

import { LMarker, LIcon, LPopup } from '@vue-leaflet/vue-leaflet';

export default {
  name: "MapMarker",
  props: {
    marker: {
      type: Object,
      required: true
    }
  },
  setup() {
    return { 
      icon_soil_moisture_blue,
      icon_soil_moisture_black,
      icon_soil_moisture_red,
      icon_temperature_blue,
      icon_temperature_black,
      icon_temperature_red,
      icon_water_level_blue,
      icon_water_level_black,
      icon_water_level_red,
      icon_water_pollution_blue,
      icon_water_pollution_black,
      icon_water_pollution_red,
      icon_sprinkler_blue,
      icon_sprinkler_black,
      icon_sprinkler_green,
      icon_sprinkler_red,
      icon_pump_blue,
      icon_pump_black,
      icon_pump_green,
      icon_pump_red,
      icon_motor_blue,
      icon_motor_black,
      icon_motor_green,
      icon_motor_red,
      icon_humidity_blue,
      icon_humidity_black,
      icon_humidity_red,
      icon_questionMark_black,
    }
  },
  components: {
    LMarker,
    LIcon,
    LPopup,
  },
  data() {
    return {
      staticAnchor: [16, 37],
      iconSize: 40,
      iconImage: icon_questionMark_black,
    }
  },
  computed: {
    dynamicSize () {
      return [this.iconSize, this.iconSize * 1.15];
    },
    dynamicAnchor () {
      return [this.iconSize / 2, this.iconSize * 1.15];
    },
  },
  mounted() {
    this.selectIcon();
  },
  methods: {
    selectIcon() {
      this.iconImage = this.findIcon();
    },
    findIcon() {
      const deviceType = this.marker.type;
      const status = this.marker.status;

      if (deviceType === "soil moisture sensor") {
        if (status === "on") { return icon_soil_moisture_blue; }
        else if (status === "off") { return icon_soil_moisture_black; }
        else { return icon_soil_moisture_red; }
      } else if (deviceType === "temperature sensor") {
        if (status === "on") { return icon_temperature_blue; }
        else if (status === "off") { return icon_temperature_black; }
        else { return icon_temperature_red; }
      } else if (deviceType === "sprinkler") {
        if (status === "on") { return icon_sprinkler_blue; }
        else if (status === "off") { return icon_sprinkler_black; }
        else if (status === "sprinkling") { return icon_sprinkler_green; }
        else { return icon_sprinkler_red; }
      }  else if (deviceType === "pump") {
        if (status === "on") { return icon_pump_blue; }
        else if (status === "off") { return icon_pump_black; }
        else if (status === "pumping") { return icon_pump_green; }
        else { return icon_pump_red; }
      } else if (deviceType === "water level") {
        if (status === "on") { return icon_water_level_blue; }
        else if (status === "off") { return icon_water_level_black; }
        else { return icon_water_level_red; }
      }  else if (deviceType === "water pollution") {
        if (status === "on") { return icon_water_pollution_blue; }
        else if (status === "off") { return icon_water_pollution_black; }
        else { return icon_water_pollution_red; }
      } else if (deviceType === "motor") {
        if (status === "on") { return icon_motor_blue; }
        else if (status === "off") { return icon_motor_black; }
        else if (status === "working") { return icon_motor_green; }
        else { return icon_motor_red; }
      } else if (deviceType === "humidity sensor") {
        if (status === "on") { return icon_humidity_blue; }
        else if (status === "off") { return icon_humidity_black; }
        else { return icon_humidity_red; }
      } else {
        return icon_questionMark_black;
      }
    },
  },
  watch: {
    marker() {
      this.selectIcon();
    },
  }
}
</script>

<style scoped>
  .marker-icon {
    height: 50px;
    width: auto;
  }
</style>