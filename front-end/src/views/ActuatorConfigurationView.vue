<template>
    <div class="configuration-page">
        <div class="left-half">
            <MapComp :inputDevices="devices" />
        </div>
        <div class="right-half">
            <h3 style="padding-top: 10px;">Actuator Rules Page</h3>
            <hr />
            <div class="graph-tab d-flex justify-content-center">
                <div class="tab">
                <button
                    v-for="tab in tabNames"
                    :key="tab"
                    :style="tabColor(tab)"
                    @click="updateSelected(tab)">
                    {{ tab }}
                </button>
                </div>
            </div>
            <br>
            <div v-if='switchTabs' class='tab1'>
                <div class="container">
                    <FormRuleSetting />
                </div>
            </div>
            <div v-if='!switchTabs' class='tab2'>
                <RulesTable />
            </div>
        </div>
    </div>
</template>

<script>
import MapComp from '@/components/Map/MapComp.vue'
import FormRuleSetting from '@/components/Form/FormRuleSetting.vue';
import RulesTable from '@/components/Table/RulesTable.vue';
import { getActuatorByType } from '@/services/actuatorService.js';
import { getRuleByActuatorId } from '@/services/ruleService.js';

export default {
    name: 'ActuatorConfigurationView',
    components: {
        MapComp,
        FormRuleSetting,
        RulesTable
    },
    data() {
        return {
            tabNames: ['ADD RULE', 'EXISTING RULES'],
            switchTabs: true,
            selectedTab: 'ADD RULE',
            devices: [
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
                }
            ],
            rules: {
                temperatureLow: "1",
                temperatureHigh: "2",
                soilMoistureLow: "3",
                soilMoistureHigh: "4",
                minute: "10",
                time: "10:00",
            },
        };
    },
    methods: {
        async getActuatorByType() {
            try {
                console.log("getActuatorByType():", this.deviceType)

                this.actuators.length = 0;
                const response = await getActuatorByType(this.deviceType);

                if (response.status !== 200) { return; }

                const data = response.data;
                this.actuators = data;
            } catch (error) {
                console.log("ActuatorConfigurationView.vue, getActuatorByType():", error);
            }
        },
        async getRuleByActuatorId() {
            try {
                console.log("getRuleByActuatorId():", this.selectedDevice)
                this.rules = {}

                const response = await getRuleByActuatorId(this.selectedDevice);

                if (response.status !== 200) { return; }

                const data = response.data;
                this.rules = data;
            } catch (error) {
                console.log("ActuatorConfigurationView.vue, getRuleByActuatorId():", error);
            }
        },
        tabColor(tabName) {
            let color = (this.selectedTab === tabName) ? "#5cbcac" : "#3fd9b3"
            return 'background-color: ' + color + ';'
        },
        updateSelected(tabName) {
            if (tabName != this.selectedTab) {
                this.selectedTab = tabName
                this.switchTabs = !this.switchTabs
            }
        }
    },
    created() {
        this.selectedTab = this.tabNames[0]
    }
}
</script>

<style scoped>
h3 {
  text-align: center;
  padding-top: 30px;
}

ActuatorSetting {
    padding-bottom: 20px;
}

.configuration-page {
    height: 100%;
}

.btn {
    width: 100px;
}

.bi {
    margin-right: 5px;
}

.left-half {
    position: absolute;
    left: 0px;
    width: 55%;
    height: 93.5%;
}

.right-half {
    position: absolute;
    right: 0px;
    width: 45%;
    padding: 10px 20px;
}

.tab {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  background-color: #3fd9b3;
  overflow: hidden;
  width: 100%;
  height: 30px;
  border: none;
  font-size: 13px;
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
</style>
