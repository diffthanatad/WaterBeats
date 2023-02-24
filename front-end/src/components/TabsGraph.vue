<template>
  <div class="graph-tab d-flex justify-content-center">
    <div class="tab">
      <button
        v-for="name in tabNames"
        :key="name"
        class="tablinks"
        :style="tabColor(name)"
        @click="updateSelected(name)">
        {{ name }}
      </button>
    </div>
  </div>
</template>

<style scoped>

* {
  font-family: 'Kumbh Sans', sans-serif;
}

.tab {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  background-color: #3fd9b3;
  overflow: hidden;
  width: 100%;
  height: 25px;
  border: none;
  font-size: 0.87vw;
}

.tab button {
  display: flex;
  border: 1px solid #fff;
  cursor: pointer;
  padding: 14px 16px;
  color: #fff;
  width: 100%;
  justify-content: center;
}

.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}
</style>

<script>
import {tabSelect} from "@/store/tab-select.js"

export default {
  name: 'TabsGraph',
  data () {
    return {
      tabNames: [],
      selectedTab: "",
      style: ''
    };
  },
  methods: {
    tabColor(name) {
      let color = (this.selectedTab === name) ? "#5cbcac" : "#3fd9b3"
      return 'background-color: ' + color + ';'
    },
    updateSelected(name) {
      tabSelect.value.setSelectedTab(name)
      this.selectedTab = tabSelect.value.selectedTab
    }
  },
  created() {
    this.tabNames = tabSelect.value.tabNames
    this.selectedTab = tabSelect.value.selectedTab
  }
}
</script>