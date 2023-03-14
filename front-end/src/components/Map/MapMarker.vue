<template>
  <div class="marker-component">
    <l-marker :lat-lng="marker.location" @click="onClickMapMarker">
      <l-icon v-if="iconImage === 1" :icon-size="dynamicSize" :icon-url="icon_soil_moisture_blue" />
      <l-icon v-else-if="iconImage === 2" :icon-size="dynamicSize" :icon-url="icon_soil_moisture_black" />
      <l-icon v-else-if="iconImage === 3" :icon-size="dynamicSize" :icon-url="icon_soil_moisture_red" />
      <l-icon v-else-if="iconImage === 4" :icon-size="dynamicSize" :icon-url="icon_temperature_blue" />
      <l-icon v-else-if="iconImage === 5" :icon-size="dynamicSize" :icon-url="icon_temperature_black" />
      <l-icon v-else-if="iconImage === 6" :icon-size="dynamicSize" :icon-url="icon_temperature_red" />
      <l-icon v-else-if="iconImage === 7" :icon-size="dynamicSize" :icon-url="icon_sprinkler_blue" />
      <l-icon v-else-if="iconImage === 8" :icon-size="dynamicSize" :icon-url="icon_sprinkler_black" />
      <l-icon v-else-if="iconImage === 9" :icon-size="dynamicSize" :icon-url="icon_sprinkler_green" />
      <l-icon v-else-if="iconImage === 10" :icon-size="dynamicSize" :icon-url="icon_sprinkler_red" />
      <l-icon v-else-if="iconImage === 11" :icon-size="dynamicSize" :icon-url="icon_pump_blue" />
      <l-icon v-else-if="iconImage === 12" :icon-size="dynamicSize" :icon-url="icon_pump_black" />
      <l-icon v-else-if="iconImage === 13" :icon-size="dynamicSize" :icon-url="icon_pump_green" />
      <l-icon v-else-if="iconImage === 14" :icon-size="dynamicSize" :icon-url="icon_pump_red" />
      <l-icon v-else-if="iconImage === 15" :icon-size="dynamicSize" :icon-url="icon_water_level_blue" />
      <l-icon v-else-if="iconImage === 16" :icon-size="dynamicSize" :icon-url="icon_water_level_black" />
      <l-icon v-else-if="iconImage === 17" :icon-size="dynamicSize" :icon-url="icon_water_level_red" />
      <l-icon v-else-if="iconImage === 18" :icon-size="dynamicSize" :icon-url="icon_water_pollution_blue" />
      <l-icon v-else-if="iconImage === 19" :icon-size="dynamicSize" :icon-url="icon_water_pollution_black" />
      <l-icon v-else-if="iconImage === 20" :icon-size="dynamicSize" :icon-url="icon_water_pollution_red" />
      <l-icon v-else :icon-size="dynamicSize" :icon-url="icon_questionMark_black" />
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

/* Import actuator icons: blue (i.e., on), green (i.e., working), black (i.e., off) and red (i.e., error). */
import icon_sprinkler_blue from "@/assets/icon/icon_sprinkler_blue.png"
import icon_sprinkler_black from "@/assets/icon/icon_sprinkler_black.png"
import icon_sprinkler_green from "@/assets/icon/icon_sprinkler_green.png"
import icon_sprinkler_red from "@/assets/icon/icon_sprinkler_red.png"
import icon_pump_blue from "@/assets/icon/icon_pump_blue.png"
import icon_pump_black from "@/assets/icon/icon_pump_black.png"
import icon_pump_green from "@/assets/icon/icon_pump_green.png"
import icon_pump_red from "@/assets/icon/icon_pump_red.png"

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
      customText: "Foobar",
      iconSize: 40,
      iconImage: 0,
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
    onClickMapMarker() {
      console.log("onClickMapMarker()", this.marker.id);
    },
    selectIcon() {
      this.iconImage = this.findIcon();
    },
    findIcon() {
      const deviceType = this.marker.type;
      const status = this.marker.status;

      if (deviceType === "soil_moisture") {
        if (status === "on") { return 1; }
        else if (status === "off") { return 2; }
        else { return 3; }
      } else if (deviceType === "temperature") {
        if (status === "on") { return 4; }
        else if (status === "off") { return 5; }
        else { return 6; }
      } else if (deviceType === "sprinkler") {
        if (status === "on") { return 7; }
        else if (status === "off") { return 8; }
        else if (status === "watering") { return 9; }
        else { return 10; }
      }  else if (deviceType === "pump") {
        if (status === "on") { return 11; }
        else if (status === "off") { return 12; }
        else if (status === "pumping") { return 13; }
        else { return 14; }
      } else if (deviceType === "water_level") {
        if (status === "on") { return 15; }
        else if (status === "off") { return 16; }
        else { return 17; }
      }  else if (deviceType === "water_pollution") {
        if (status === "on") { return 18; }
        else if (status === "off") { return 19; }
        else { return 20; }
      }
    },
  },
  watch: {
  }
}
</script>

<style scoped>
/* .marker-icon {
    height: 50px;
    width: auto;
  }
  .leaflet-popup-content-wrapper {
    width: 300px;
  }
  .fas {
    margin-right: 10px;
  }
  div {
    font-size: 16px;
  } */
  .marker-icon {
    height: 50px;
    width: auto;
  }
</style>