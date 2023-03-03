import {ref} from "vue";

export const tabSelect = ref({
    tabNames: ["temperature", "soil_moisture", "water_pollution", "water_level"],
    selectedTab: "temperature",
    setSelectedTab(name) {
        this.selectedTab = name
    }
});