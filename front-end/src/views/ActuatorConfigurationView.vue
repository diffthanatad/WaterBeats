<template>
    <div class="configuration-page d-flex flex-row">
        <div class="left-half">
            <MapComp></MapComp>
        </div>
        <div class="right-half">
            <div class="row">
                <div class="col-6">
                    <Field class="form-select" name="field" as="select" v-model="deviceType"
                        aria-label="Default select example">
                        <option value="pump">Pump</option>
                        <option value="sprinkler">Sprinkler</option>
                    </Field>
                </div>
                <div class="col-6">
                    <button type="button" class="btn btn-primary col-6" @click.prevent="searchDeviceByActuatorType">
                        <i class="bi bi-search"></i>Search
                    </button>
                </div>
            </div>
            <hr />
            <h3> Rules </h3>
            <!-- <form @submit.prevent="onSubmit">
                <input type="email" name="email" />
                <button>Sign up for newsletter</button>
            </form> -->
            <!-- <Form @submit="onSubmit">
                <Field name="email" type="email" rules="required"/>
                <ErrorMessage name="email" />
                <button>Sign up for newsletter</button>
            </Form> -->
            <Form @submit="onSubmitRule">
                <div class="mb-3 row">
                    <label for="inputTemperatureLow" class="col-sm-6 col-form-label">Turn on when temperature is</label>
                    <div class="col-sm-2">
                        <Field class="form-control" name="temperatureLow" v-model="temperatureLow"
                            rules="required" />
                        <ErrorMessage name="temperatureLow" />
                    </div>
                    <div class="col-sm-2">
                        <Field class="form-control" name="temperatureHigh" v-model="temperatureHigh"
                            :rules="validateNumber" />
                        <ErrorMessage name="temperatureHigh" />
                    </div>
                </div>
                <button class="btn btn-primary">Save</button>
            </Form>
        </div>
    </div>
</template>

<script>
import MapComp from '@/components/Map/MapComp.vue'
import { Form, Field, ErrorMessage, } from 'vee-validate';

export default {
    name: 'ActuatorConfigurationView',
    components: {
        MapComp,
        Field,
        Form,
        ErrorMessage,
    },
    data() {
        return {
            deviceType: "pump",
            temperatureLow: 0,
            temperatureHigh: 0,
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            center: [51.52498676710948, -0.1344647153442085], /* University College London */
            attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            zoom: 16,
            interval: 7,
            sensors: [
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
    methods: {
        searchDeviceByActuatorType() {
            console.log("searchDeviceByActuatorType()", this.deviceType);
        },
        validateNumber(value) {
            if (!value) { return 'This field is required'; }
            const regex = /^(0|[1-9]\d*)(\.\d+)?$/;
            if (!regex.test(value)) { return 'This field must be a valid number'; }
            return true;
        },
        // onSubmitRule(values) {
        //     console.log(JSON.stringify(values, null, 2));
        // }
        validateEmail(value) {
            // if the field is empty
            if (!value) {
                return 'This field is required';
            }
            // if the field is not a valid email
            const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;
            if (!regex.test(value)) {
                return 'This field must be a valid email';
            }
            // All is good
            return true;
        },
        onSubmitRule(values) {
            console.log(values);
        },
        onSubmit(value) {
            console.log('Submitted', value);
        },
    },
}
</script>

<style scoped>
/* .map {
    width: 47% !important;
    height: 90% !important;
} */
.configuration-page {}

.form-select {
    /* width: 200px; */
}

.btn {
    width: 100px;
}

.bi {
    margin-right: 5px;
}

.left-half {
    background-color: #ff9e2c;
    position: absolute;
    left: 0px;
    width: 50%;
    height: 100%;
}

.right-half {
    background-color: #b6701e;
    position: absolute;
    right: 0px;
    width: 50%;
    padding: 10px 20px;
}
</style>>
