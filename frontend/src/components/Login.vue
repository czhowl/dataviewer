<template>
   <div >
         <div class="container">
          <gmap-map
            :center="center"
            :options="options"
            :zoom="7"
            :map-type-id="mapTypeId"
            v-bind:style="background"
            ref="bgmap"
          >
          </gmap-map>
            <div class="container center">
               <h1 class="noselect" id="title">NVH DataViewer</h1>
                <div v-if="this.$store.state.loading" class="loader"><grid-loader :loading="loader.loading" :color="loader.color" :size="loader.size" class="loading-icon"></grid-loader></div>
               <div v-else>
                <div class="form-group form-login">
                    <input class="form-control form-input" name="username" type="text" placeholder="Username" v-model="username"
                           required pattern="\w{3,12}"/>
                </div>
                <div class="form-group form-login">
                    <input class="form-control form-input" name= "password" type="password" placeholder="Password" v-model="password"
                           required pattern="\w{4,}"/>
                </div>
                <div v-if="errorCode == 1" class="form-group form-login prompt">Invalid email address</div>
                <div v-if="errorCode == 2" class="form-group form-login prompt">Password must be at least 6 4~12 a-z, 0-9 or _</div>
                <div class="form-group clearfix form-login" @submit.prevent>
                    <input type="submit" @click="login()" class="btn btn-warning btn-login" value="Log In" />
                    <input type="submit" @click="register()" class="btn btn-warning btn-register" value="[alpha]Register" />
                </div>
                </div>
        </div>
         </div>
   </div>
</template>

<script>
    export default {
        mounted() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    this.center.lat = position.coords.latitude;
                    this.center.lng = position.coords.longitude;
                })
            }
            this.$nextTick(function() {
                window.addEventListener('resize', this.reCenter);
                window.addEventListener("orientationchange", this.reCenter);
            })
        },
        beforeDestroy() {
            window.removeEventListener('resize', this.reCenter);
            window.removeEventListener("orientationchange", this.reCenter);
        },
        computed: {
            validation() {
                var patt1 = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                var patt2 = /(\w{6,})/
                if (!patt1.test(this.username)) {
                    this.errorCode = 1
                    return false
                } else if (!patt2.test(this.password)) {
                    this.errorCode = 2
                    return false
                } else {
                    this.errorCode = 0
                    return true
                }
            }
        },
        methods: {
            login: function() {
                if (!this.validation) return;
                this.$store.dispatch('loading', true);
                var csrf_token = '';

                this.$http.get('/login').then((response) => {
                    // 响应成功回调
                    var data = response.body;
                    var csrf_token = '';
                    try {
                        csrf_token = data.match(/name="csrf_token" type="hidden" value="(.*?)">/)[1];
                        //                    alert(csrf_token);
                    } catch (exception) {
                        // 如果已经登陆，则302，redirect to home
                        alert(exception); // exception: TypeError: Cannot read property '1' of null
                        alert('something wrong...');
                        this.$store.dispatch('loading', false);
                        return window.location = '/logout';
                    }

                    this.$http.post('/login',
                        //body
                        {
                            email: this.username,
                            password: this.password,
                            csrf_token: csrf_token
                        },
                        //options
                        {
                            headers: {
                                'Content-Type': 'application/json; charset=UTF-8'
                            }
                        }).then((response) => {
                        // 响应成功回调
                        var jsondata = response.body;
                        //alert(JSON.stringify(jsondata));
                        this.token = jsondata.response.user.authentication_token
                        this.isLogin = true
                        //               alert('token:\n'+ this.token);
                        var userData = {
                            'username': this.username,
                            'authentication_token': this.token
                        };
                        this.$store.dispatch('logInUser', userData);
                        window.localStorage.setItem("user", JSON.stringify(userData));
                        //     this.$nextTick(function () { });
                        //   getSubscription()
                    }, (response) => {
                        // 响应Login-POST错误回调
                        this.$store.dispatch('loading', false);
                        alert('登录出错了！ ' + response.status + response.statusText)
                    });
                }, (response) => {
                    // 响应login-GET 错误回调
                    this.$store.dispatch('loading', false);
                    alert('登录出错了(CSRF)！ ' + JSON.stringify(response))
                });
            },
            reCenter(event) {
                this.$refs.bgmap.resizePreserveCenter();
            },
            register() {
                if (!this.validation) return;
                // get CSRF
                var csrf_token = '';
                this.$http.get('/register').then((response) => {
                    // 响应成功回调
                    var data = response.body;
                    // <input id="csrf_token" name="csrf_token" type="hidden" value="1483433916##5b057abdef66da070c8385752b78f6c584f6ba41"><input
                    var csrf_token = data.match(/name="csrf_token" type="hidden" value="(.*?)">/)[1]
                    //              alert(csrf_token);                
                    this.$http.post('/register',
                        //body
                        {
                            email: this.username,
                            password: this.password,
                            csrf_token: csrf_token
                        },
                        //options
                        {
                            headers: {
                                'Content-Type': 'application/json; charset=UTF-8'
                            }
                        }).then((response) => {
                        // 响应成功回调
                        var data = response.body;
                        //          alert('Server rsp:\n'+ JSON.stringify(response));
                        //"body":{"meta":{"code":400},"response":{"errors":{"email":["aaa@bbb.com is already associated with an account."]}}},
                        if (data.meta.code !== 200) {
                            return alert(JSON.stringify(data.response.errors))
                        }
                        this.token = data.response.user.authentication_token;
                        this.isLogin = true;
                        
                        this.$store.state.lastSync = 'never updated before'  
                        var userData = {
                            'username': this.username,
                            'authentication_token': this.token
                        };
                        this.$store.dispatch('firstTime', true)
                        this.$store.dispatch('logInUser', userData);
                    }, (response) => {
                        // 响应错误回调
                        alert('注册出错了！ ' + JSON.stringify(response))
                    });
                }, (response) => {
                    // 响应register-GET 错误回调
                    alert('注册出错了(CSRF)！ ' + JSON.stringify(response))
                });
            }
        },
        data() {
            return {
                loader: {
                    color: "azure",
                    size: "5px",
                    loading: true,
                },
                errorCode: 0,
                isLogin: false,
                username: '',
                password: '',
                background: {
                    zIndex: "-1",
                    position: "fixed",
                    width: "100%",
                    height: "100vh",
                    left: "0px",
                    backgroundColor: "#99291b",
                },
                h1style: {
                    zIndex: "100",
                    fontFamily: "Helvetica Neue",
                    fontWeight: "100",
                    color: "white",
                    position: "absolute",
                    top: "30%",
                    textAlign: "center",
                    width: "100%",
                    left: "0px",
                },
                center: {
                    lat: 40,
                    lng: -86,
                },
                options: {
                    draggable: false,
                    scrollwheel: false,
                    panControl: false,
                    clickableIcons: false,
                    disableDoubleClickZoom: true,
                    fullscreenControl: false,
                    keyboardShortcuts: false,
                    streetViewControl: false,
                    scaleControl: false,
                    zoomControl: false,
                    mapTypeControl: false,
                    backgroundColor: "#99291b",
                    styles: [{
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#c2442c"
                        }]
                    }, {
                        "elementType": "labels.icon",
                        "stylers": [{
                            "visibility": "off"
                        }]
                    }, {
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#e67f5b"
                        }]
                    }, {
                        "elementType": "labels.text.stroke",
                        "stylers": [{
                            "color": "#a83c2d"
                        }]
                    }, {
                        "featureType": "administrative.land_parcel",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#bdbdbd"
                        }]
                    }, {
                        "featureType": "poi",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#ee5128"
                        }]
                    }, {
                        "featureType": "poi",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#75270b"
                        }]
                    }, {
                        "featureType": "poi.park",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#c6552a"
                        }]
                    }, {
                        "featureType": "poi.park",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#c0160d"
                        }]
                    }, {
                        "featureType": "road",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#b33b16"
                        }]
                    }, {
                        "featureType": "road.arterial",
                        "elementType": "labels",
                        "stylers": [{
                            "visibility": "off"
                        }]
                    }, {
                        "featureType": "road.arterial",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#750510"
                        }]
                    }, {
                        "featureType": "road.highway",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#c13410"
                        }]
                    }, {
                        "featureType": "road.highway",
                        "elementType": "labels",
                        "stylers": [{
                            "visibility": "off"
                        }]
                    }, {
                        "featureType": "road.highway",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#c3001b"
                        }]
                    }, {
                        "featureType": "road.local",
                        "stylers": [{
                            "visibility": "off"
                        }]
                    }, {
                        "featureType": "road.local",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#9e0004"
                        }]
                    }, {
                        "featureType": "transit.line",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#e57031"
                        }]
                    }, {
                        "featureType": "transit.station",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#ee3e16"
                        }]
                    }, {
                        "featureType": "water",
                        "elementType": "geometry",
                        "stylers": [{
                            "color": "#99291b"
                        }]
                    }, {
                        "featureType": "water",
                        "elementType": "labels.text.fill",
                        "stylers": [{
                            "color": "#ff4c3d"
                        }]
                    }]
                },
                mapTypeId: "terrain"
            }
        }
    }

</script>

<style scoped="true">
    .noselect {
        -webkit-touch-callout: none;
        /* iOS Safari */
        -webkit-user-select: none;
        /* Safari */
        -khtml-user-select: none;
        /* Konqueror HTML */
        -moz-user-select: none;
        /* Firefox */
        -ms-user-select: none;
        /* Internet Explorer/Edge */
        user-select: none;
        /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
    }
    
    .center {
        font-family: Helvetica Neue;
        font-weight: 200;
        top: 50%;
        position: fixed;
        display: block;
        width: 400px;
        height: 300px;
        left: 50%;
        margin: -150px 0 0 -200px;
        vertical-align: middle;
        text-align: center;
    }
    
    .loader {
        position: relative;
        left: 50%;
        margin-left: -5px;
        top: 15%;
    }
    
    .form-login {
        width: 266.67px;
        display: table;
        margin: 15px auto;
    }
    
    .btn-login {
        font-family: Helvetica Neue;
        font-weight: 200;
        width: 150px;
        left: 80px;
        margin: 0 -75px auto;
        position: relative;
        background-color: #c71313;
        border-color: #dbdbdb;
        transition: background-color 0.1s;
        transition-timing-function: ease-in;
    }
    
    .btn-login:hover {
        background-color: #e68981;
    }
    
    .btn-login:active {
        border-color: #dbdbdb;
    }
    
    .btn-register {
        font-family: Helvetica Neue;
        font-weight: 200;
        width: 150px;
        left: -80px;
        margin: 0 -75px auto;
        position: relative;
        background-color: #cc920e;
        border-color: #dbdbdb;
        transition: background-color 0.1s;
        transition-timing-function: ease-in;
    }
    
    .btn-register:hover {
        background-color: #e6ac81;
    }
    
    .btn-register:active {
        border-color: #dbdbdb;
    }
    
    .form-input {
        transition: border-color 0.1s;
        transition-timing-function: ease-in;
    }
    
    .form-input:focus {
        border-color: #dbdbdb;
    }
    
    .prompt {
        font-size: 0.8em;
        color: aliceblue;
    }
    
    h1 {
        font-family: Helvetica Neue;
        font-weight: 100;
        font-size: 3.5em;
        color: azure;
        text-align: center;
        width: 100%;
        left: 0px;
        margin-bottom: 40px;
    }

</style>
