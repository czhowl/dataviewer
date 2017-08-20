import Vue from 'vue'
import * as types from './mutation-types'

export default {
    logInUser: function({ commit }, userData) {
        commit(types.LOG_IN, userData)
    },
    updateLastSync: function({ commit }, timestamp) {
        commit(types.UPDATE_LAST_SYNC, timestamp)
    },
    logOutUser: function({ commit }) {
        commit(types.LOG_OUT)
    },
    loadRoadData: function ({ commit }, [userInfo, zoom]) {
        Vue.http.get('/api/get-data', {
                    params: {
                        email: userInfo.username
                    },
                    headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Authentication-Token': userInfo.token
                    }
                }).then((response) => {
                    // 响应成功回调
                    var data = response.body
                    commit(types.LOAD_ROAD_DATA, data)
                }, (response) => {
                    // 响应错误回调
                    alert('wrong!' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('timeout');
                        //this.$store.dispatch('logOutUser')
                    }
                });
    },
    loading: function ({ commit }, isLaoding) {
        commit(types.LOADING, isLaoding)
    },
    firstTime: function ({ commit }, isFirstTIme) {
        commit(types.FIRST_TIME, isFirstTIme)
    },
    updateVehicleInfo: function ({ commit }, vehicle) {
        commit(types.UPDATE_VEHICLE_INFO, vehicle)
    }
}