import { getAllAlerts } from '@/services/alertService'


const getDefaultState = () => {
  return {
    alertList: []
  }
}
const state = getDefaultState();

const mutations = {
    RESET_STATE() {
        state.alertList = []
    },
    setAlertList(state, alertList) {
        state.alertList = alertList
    }
};

const actions = {
    async updateAlertList({ commit }) {
        const response = await getAllAlerts()

        if (response.status != 200) {
            commit('RESET_STATE')
            return
        }
        let alertList = []
        const alerts = response.data.data

        for (const alert of alerts) {
            alertList.push(alert)
        }
        commit('setAlertList', alertList)
    }
};

export default {
    namespaced: true,
    state,
    mutations,
    actions
}
