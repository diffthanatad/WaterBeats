const getDefaultState = () => {
    return {
        devices: [],
        automatic: false,
    }
}

const state = getDefaultState();

const mutations = {
    CLEAR_DEVICE(state) {
        state.devices = [];
    },
    RESET_STATE(state) {
        Object.assign(state, getDefaultState());
    },
    UPDATE_DEVICE(state, item) {
        state.devices = item;
    },
    START_AUTOMATIC(state) {
        state.automatic = true;
    }
};

const actions = {
    update(state, item) {
        state.commit('CLEAR_DEVICE');
        state.commit('UPDATE_DEVICE', item);
    },
    clear(state) {
        state.commit('RESET_STATE');
    },
    start(state) {
        state.commit('START_AUTOMATIC');
    },
};

const getters = {
    getDevices: (state) => {
        return state.devices;
    },
    getAutomatic: (state) => {
        return state.automatic;
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}