import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'
import getters from './getters'

Vue.use(Vuex);

const state = {
    logIn: false,
    firstTime: false,
    lastSync: '',
    lastSyncTime: '',
    userInfo: {
        token: '',
        username: '',
    },
    vehicle: {
        weight: '',
        tire_pressure: '',
        make: "",
        model: "",
        year: ''
    },
    roadData: {
        data: [],
        gps:[]
    },
    filter: {
        date: [],
    },
    loading: true,
    status: ''
};

export default new Vuex.Store({
    state,
    mutations,
    actions,
    getters
})
