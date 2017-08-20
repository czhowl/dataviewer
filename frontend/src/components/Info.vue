<template>
  <div class="card">
       <div class="switch" title="switch device"><span class="option-text">Switch Device</span><i class="fa fa-exchange option" aria-hidden="true"></i></div>
        <div class="card-header" align="center">
           <div class="device-img">
            <img src="/static/img/avatar.png"
                 class="thumbnail" />
            </div>
            <p class="device-info device-name">{{ deviceName }}</p>
            <p class="device-info">{{ this.$store.state.userInfo.username }}</p>
            <p class="device-info">Last Update: <span style="white-space: nowrap;">{{ this.$store.state.lastSync }}</span></p>
        </div>
        <div class="" style="text-align: right;" @click="setting">
               <i class="fa fa-cog settings" aria-hidden="true" title="Settings" ></i>
           </div>
        <div v-if="!editing" class="card-block">
            <span class="info-text-title">Gross Vehicle Weight: </span>
            <span class="info-text">{{ this.$store.state.vehicle.weight }} lbs.</span>
            <hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Tire Pressure: </span>
            <span class="info-text">{{ this.$store.state.vehicle.tire_pressure }} psi.</span>
            <hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Make: </span><span class="info-text">{{ this.$store.state.vehicle.make }}</span><hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Model: </span><span class="info-text">{{ this.$store.state.vehicle.model }}</span><hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Model Year: </span><span class="info-text">{{ this.$store.state.vehicle.year }}</span>
        </div>
        <div v-else class="card-block">
            <span class="info-text-title">Gross Vehicle Weight: </span>
            <span class="info-text"><input type= "number" min="1" :max="20000" class="form-control filter-input-number" v-model="info.weight" v-on:blur="if(info.weight>20000){info.weight=20000}else if(info.weight<1){info.weight=1}"> lbs.</span>
            <hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Tire Pressure: </span>
            <span class="info-text"><input type="number" min="10" :max="150" class="form-control filter-input-number psi" v-model="info.tire_pressure" v-on:blur="if(info.tire_pressure>150){info.tire_pressure=150}else if(info.tire_pressure<10){info.tire_pressure=10}"> psi.</span>
            <hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Make: </span><span class="info-text"><select class="filter-input-number dropdown"  id="make" name="make" v-model="info.make">
                <option v-for="option in Object.keys(makemodel)" v-bind:value="option">
                    {{ option }}
                </option>
            </select></span><hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Model: </span><span class="info-text"><select class="filter-input-number dropdown"  id="make" name="make" v-model="info.model">
                <option v-for="option in makemodel[info.make]" v-bind:value="option">
                    {{ option }}
                </option>
            </select></span><div v-if="errorCode == 1" class="prompt">Please select vehicle model.</div><hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <span class="info-text-title">Model Year: </span><span class="info-text"><input type= "number" min="1900" :max="2100" class="form-control filter-input-number year" v-model="info.year" v-on:blur="if(info.year>2100){info.year=2100}else if(info.year<1900){info.year=1900}"></span>
            <hr style="margin-top: 0.3em; margin-bottom: 0.1em;">
            <button :disabled="this.$store.state.firstTime" v-on:click="settingCancel" class="btn-setting btn-cancel">Cancel</button>
            <button v-on:click="settingSave" class="btn-setting btn-save">Save</button>
        </div>
        
    </div>
</template>




<script>
    import {
        auto_info
    } from './Auto'
    export default {
        components: {},
        created() {
            this.getInfo()
        },
        mounted() {

        },
        beforeDestroy() {

        },
        computed: {
            validation() {
                if (!auto_info[this.info.make].includes(this.info.model)) {
                    this.errorCode = 1
                    return false
                } else if (_.isEqual(this.$store.state.vehicle, this.info)) {
                    this.settingCancel()
                    return false
                } else {
                    this.errorCode = 0
                    return true
                }
            }
        },
        methods: {
            setting: function() {
                if (this.editing) {
                    this.settingCancel()
                } else {
                    this.editing = true
                    this.info = JSON.parse(JSON.stringify(this.$store.state.vehicle))
                }
            },
            settingSave: function() {
                if (!this.validation) return;
                this.$store.dispatch('loading', true);
                this.$http.post('/api/vehicle',
                    //body
                    {
                        email: this.$store.state.userInfo.username,
                        vehicle: this.info
                    },
                    //options
                    {
                        headers: {
                            'Content-Type': 'application/json; charset=UTF-8',
                            'Authentication-Token': this.$store.state.userInfo.token
                        }
                    }).then((response) => {
                    // success
                    var data = response.body
                    this.$store.dispatch('updateVehicleInfo', this.info)
                    this.editing = false
                    this.$store.dispatch('firstTime', false)
                    this.$store.dispatch('loading', false);
                }, (response) => {
                    // error
                    alert('error！ ' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('timeout, please login again');
                    }
                });
            },
            settingCancel: function() {
                this.editing = false
            },
            getInfo: function() {
                this.$http.get('/api/vehicle', {
                    params: {
                        email: this.$store.state.userInfo.username
                    },
                    headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                        'Authentication-Token': this.$store.state.userInfo.token
                    }
                }).then((response) => {
                    // get
                    var data = response.body
                    if (!data.lastSync) {
                        this.$store.state.lastSync = 'never updated before'
                    } else {
                        this.$store.dispatch('updateLastSync', data.lastSync)
                    }
                    if (data == 'None') {
                        this.$store.dispatch('firstTime', true)
                        this.editing = true
                    } else {
                        this.$store.dispatch('updateVehicleInfo', data)
                        this.info = data
                    }
                    this.$store.dispatch('loading', false);
                }, (response) => {
                    // get
                    alert('get vehicle info error! ' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('timeout');
                    }
                });
            }
        },
        data() {
            return {
                errorCode: 0,
                makemodel: auto_info,
                editing: false,
                deviceName: "NVH Device Prototype",
                info: {
                    weight: '',
                    tire_pressure: '',
                    make: "",
                    model: "",
                    year: ''
                },
            }
        },
    }

</script>

<style scoped="true">
    .prompt {
        font-family: Helvetica Neue;
        font-size: 0.7em;
        font-weight: 400;
        color: #bf4031;
        margin-top: 5px;
    }
    
    .card-block {
        padding-top: 0px;
    }
    
    .btn-setting {
        text-align: center;
        height: 33px;
        font-size: 0.8em;
        font-family: Helvetica Neue;
        width: 55px;
        height: 23px;
        border-radius: 3px;
        border: 0;
        display: table-cell;
        vertical-align: middle;
        margin-top: 5px;
        transition: background-color 0.3s;
    }
    
    .btn-save {
        float: right;
        right: 10px;
        color: azure;
        background-color: #bf4031;
        font-weight: 100;
        cursor: pointer;
    }
    
    .btn-save:hover {
        background-color: #99291b;
    }
    
    .btn-cancel {
        float: left;
        left: 10px;
        color: #85858e;
        cursor: pointer;
    }
    
    .btn-cancel:hover {
        background-color: #a4a4af;
    }
    
    .filter-input-number {
        font-size: 0.8em;
        font-family: Helvetica Neue;
        font-weight: 200;
        border: 0;
        padding: 0 0 0 5px;
        display: inline;
        width: 53px;
        height: 20px;
    }
    
    .switch {
        text-align: right;
        vertical-align: middle;
        background-color: #bf4031;
        transition: background-color 0.3s;
        border-radius: 3px 3px 0 0;
        cursor: pointer;
    }
    
    .switch:hover {
        background-color: #99291b;
    }
    
    .info-text {
        white-space: nowrap;
        font-family: Helvetica Neue;
        font-weight: 400;
        font-size: 0.8em;
    }
    
    i.settings {
        color: #a39f9f;
        margin: 4px;
        transition: color 0.3s;
        cursor: pointer;
    }
    
    i.settings:hover {
        color: #6f6262;
    }
    
    .option {
        color: azure;
        margin: 4px;
    }
    
    p.device-info {
        font-family: Helvetica Neue;
        font-weight: 200;
        font-size: 0.7em;
        margin-bottom: 5px;
    }
    
    p.device-name {
        font-family: Helvetica Neue;
        font-weight: 400;
        font-size: 0.8em;
    }
    
    span.info-text-title {
        font-family: Helvetica Neue;
        font-weight: 400;
        font-size: 0.7em;
        color: #78828b;
    }
    
    .option-text {
        font-family: Helvetica Neue;
        font-weight: 200;
        font-size: 0.8em;
        color: azure;
        margin: 4px 0 4px 4px;
    }
    
    .card {
        background-color: #d8d8d8;
        height: 100%;
        box-shadow: 1px 1px 2px rgba(0, 0, 0, .3);
    }
    
    .thumbnail {
        object-fit: cover;
        width: 75px;
        height: 75px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    .psi {
        width: 40px;
    }
    
    .year {
        width: 45px;
    }
    
    .dropdown {
        width: 90px;
    }

</style>
