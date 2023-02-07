<template>
  <div class="marker-component">
    <l-marker :lat-lng="marker.location">
      <!-- <l-icon :lat-lng="marker.location" :icon-anchor=[0,0]> -->
        <!-- <img v-if="iconImage === 1" class="marker-icon" src="@/assets/icon_water_blue.png" style=""/>
        <img v-else-if="iconImage === 2" class="marker-icon" src="@/assets/icon_water_black.png" style=""/>
        <img v-else-if="iconImage === 3" class="marker-icon" src="@/assets/icon_water_red.png" style=""/>
        <img v-else-if="iconImage === 4" class="marker-icon" src="@/assets/icon_temperature_blue.png" style=""/>
        <img v-else-if="iconImage === 5" class="marker-icon" src="@/assets/icon_temperature_black.png" style=""/>
        <img v-else-if="iconImage === 6" class="marker-icon" src="@/assets/icon_temperature_red.png" style=""/> -->
        <!-- <img class="marker-icon" :src="deviceIcon" /> -->
        <!-- <img class="marker-icon" :src="`${selectIcon}" /> -->
      <!-- </l-icon> -->
      <l-icon
          :icon-size="dynamicSize"
          :icon-url="icon_water_black"
        />
      <l-popup style="width: 250px;">
        <div>
          <h5 style="text-align: center;"><i class="fas fa-tablet-alt"></i>{{ marker.type }} {{ iconImage }}</h5>
          <div class="row">
            <div class="col-4"><i class="bi bi-clock"></i></div>
            <div class="col-8"> {{ marker.timestamp ? marker.timestamp : "N/A" }} </div>
          </div>
          <div class="row">
            <div class="col-4">Value</div>
            <div class="col-8"> {{ marker.value ? marker.value : "N/A" }} </div>
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
import icon_water_black from '@/assets/icon_water_black.png'
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
    return { icon_water_black }
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
      iconSize: 64,
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
    selectIcon() {
      this.iconImage = this.findIcon();
    },
    findIcon() {
      const deviceType = this.marker.type;
      const status = this.marker.status;

      if (deviceType === "Soil Moisture Sensor") {
        if (status === "on") { return 1; }
        else if (status === "off") { return 2; }
        else if (status === "error") { return 3; }
      } else if (deviceType === "Temperature Sensor") {
        if (status === "on") { return 4; }
        else if (status === "off") { return 5; }
        else if (status === "error") { return 6; }
      } else if (deviceType === "Water Springkler") {
        return '@/assets/icon_water_black.png';
      } else {
        return '@/assets/icon_water_black.png';
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