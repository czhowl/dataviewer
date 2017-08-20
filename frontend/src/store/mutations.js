import * as types from './mutation-types'

export default {
    // 在搜索列表中，订阅某公众号
    [types.LOAD_ROAD_DATA](state, data) {
        state.roadData.data = data
        state.roadData.gps = data.map(function(a) {return {lat: a.lat, lng: a.lng};});
    },
    [types.LOG_IN](state, userData) {
        state.logIn = true
        state.userInfo.token = userData.authentication_token
        state.userInfo.username = userData.username
    },
    [types.UPDATE_LAST_SYNC](state, timestamp) {
        if (timestamp != '') {
            state.lastSyncTime = timestamp
            var time = Date.parse(timestamp)
        } else {
            var time = Date.parse(state.lastSyncTime)
        }
        time = Date.now() - time
        var secs = time / 1000 % 60;
        time = (time / 1000 - secs) / 60;
        var mins = time % 60;
        var hrs = (time - mins) / 60;
        if (hrs > 168) {
            var week = Math.floor(hrs / 168)
            if (week == 1) {
                state.lastSync = 'a week ago'
            } else {
                state.lastSync = week + ' weeks ago'
            }
        } else if (hrs > 24) {
            //days ago
            var day = Math.floor(hrs / 24)
            if (day == 1) {
                state.lastSync = '1 day ago'
            } else {
                state.lastSync = day + ' days ago'
            }
        } else if (hrs > 0) {
            //hours ago
            if (hrs == 1) {
                state.lastSync = '1 hour ago'
            } else {
                state.lastSync = hrs + ' hours ago'
            }
        } else if (mins > 0) {
            //minutes ago
            if (mins == 1) {
                state.lastSync = '1 minute ago'
            } else {
                state.lastSync = mins + ' minutes ago'
            }
        } else {
            //less than a minutes
            state.lastSync = 'less than 1 minute'
        }
    },
    [types.LOG_OUT](state) {
        state.logIn = false
        state.lastSync = ''
        state.lastSyncTime = ''
        state.userInfo.token = ''
        state.userInfo.username = ''
        state.status = 'Logged out'
        state.vehicle = ''
    },
    [types.LOADING](state, isLoading) {
        state.loading = isLoading
        if (isLoading) {
            state.status = 'Loading data'
        } else {
            state.status = 'Ready'
        }
    },
    [types.FIRST_TIME](state, isFirstTIme) {
        state.firstTime = isFirstTIme
    },
    [types.UPDATE_VEHICLE_INFO](state, vehicleInfo) {
        state.vehicle = vehicleInfo
    },
};
