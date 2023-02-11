<template>
    <!-- <div class="mb-3 row">
        <label for="inputTemperatureLow" class="col-sm-5 col-form-label">{{ label }}</label>
        <div class="col-3">
            <div class="input-group mb-3">
                <span class="input-group-text" id="basic-addon1">{{ firstInputLabel }} {{ firstInputInitialValue }}</span>
                <Field class="form-control" aria-label="temperatureLow" aria-describedby="basic-addon1"
                    name="firstInput" v-model="firstInputValue" rules="required" :placeholder="firstPlaceholder" disabled />
                <ErrorMessage name="firstInput" />
            </div>
        </div>
        <div class="col-3">
            <div class="input-group mb-3">
                <span class="input-group-text" id="basic-addon1">{{ secondInputLabel }} {{ secondInputInitialValue }}</span>
                <Field class="form-control" aria-label="temperatureHigh" aria-describedby="basic-addon1"
                    name="secondInput" v-model="secondInputValue" rules="required" :placeholder="secondPlaceholder" disabled/>
                <ErrorMessage name="secondInput" />
            </div>
        </div>
    </div> -->
    <div class="mb-3 row">
        <label for="inputTemperatureLow" class="col-sm-5 col-form-label">{{ label }}</label>
        <div class="col-3">
            <div class="input-group mb-3">
                <span class="input-group-text" id="basic-addon1">{{ firstInputLabel }}</span>
                <input class="form-control" aria-label="temperatureLow" aria-describedby="basic-addon1"
                    name="firstInput" v-model="firstInputValue" :placeholder="firstPlaceholder" />
            </div>
        </div>
        <div class="col-3">
            <div class="input-group mb-3">
                <span class="input-group-text" id="basic-addon1">{{ secondInputLabel }}</span>
                <input class="form-control" aria-label="temperatureHigh" aria-describedby="basic-addon1"
                    name="secondInput" v-model="secondInputValue" :placeholder="secondPlaceholder" />
            </div>
        </div>
    </div>
</template>
  
<script>
// import { Field, ErrorMessage, } from 'vee-validate';

export default {
    name: 'RuleSettingForm',
    components: {
        // Field,
        // ErrorMessage,
    },
    props: {
        label: {
            type: String,
            required: true,
        },
        firstInputLabel: {
            type: String,
            required: true,
        },
        firstPlaceholder: {
            type: String,
            required: true,
        },
        firstInputInitialValue: {
            type: String,
            required: true,
        },
        secondInputLabel: {
            type: String,
            required: true,
        },
        secondPlaceholder: {
            type: String,
            required: true,
        },
        secondInputInitialValue: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            firstInputValue: this.firstInputInitialValue,
            secondInputValue: this.secondInputInitialValue,
        }
    },
    methods: {

    },
    watch: {
        firstInputValue (value) {
            const obj = {
                firstInputValue: value,
                secondInputValue: this.secondInputValue,
            }
            this.$emit('onChangeInputValue', obj);
        },
        secondInputValue (value) {
            const obj = {
                firstInputValue: this.firstInputValue,
                secondInputValue: value,
            }
            this.$emit('onChangeInputValue', obj);
        }
    }
};
</script>
  
<style>

</style>