const getDefaultState = () => {
    return {
        devices: []
    }
}

const state = getDefaultState();

const mutations = {
    RESET_STATE(state) {
        Object.assign(state, getDefaultState());
    },
    UPDATE_DEVICE(state, item) {
        state.devices = item;
    },
};

const actions = {
    update(state, item) {
        state.commit('RESET_STATE');
        state.commit('UPDATE_DEVICE', item);
    },
    clear(state) {
        state.commit('RESET_STATE');
    },
};

const getters = {
    getDevices: (state) => {
        return state.devices;
    },
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}