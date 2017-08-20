<template>
   <div class="card" id="mapView">
       <div class="title"><i class="fa fa-map-o" aria-hidden="true"></i><span class="option-text">Map</span><div class="corner-icon">
       <i class="fa fa-exchange option-icon" title="Change view" aria-hidden="true" @click="$emit('switch')"></i>
       <transition name="expand" mode="out-in">
       <i v-if="!fullView" class="fa fa-expand option-icon" title="Maximize" key="max" aria-hidden="true" @click="expand"></i>
       <i v-else class="fa fa-compress option-icon" title="Minimize" key="min" aria-hidden="true" @click="expand"></i>
       </transition>
    </div></div>
     <div class="toolbox" align="center">
           <div title="Select" v-on:click="resizeMap" class="tool">
    <i class="fa fa-mouse-pointer" aria-hidden="true"></i>
  </div>
        </div>

  <gmap-map
    :center="center"
    :zoom="14"
    :style="mapstyle"
    :options="options"
    ref="datamap"
  >
  <gmap-polyline :path="this.$store.state.roadData.gps" :draggable="false" :editable="false" @click="" :deepWatch=false :options="rawline2"></gmap-polyline>
  <gmap-polyline :path="this.$store.state.roadData.gps" :draggable="false" :editable="false" @click="" :deepWatch=false :options="rawline1"></gmap-polyline>
  </gmap-map>
    </div>
</template>

<script>
    import {
        mapState
    } from 'vuex'
    export default {
        props: {
            expanded: {
                type: Boolean,
                default: false,
            }
        },
        computed: mapState([
            'roadData'
        ]),
        watch: {
            expanded: function(val) {
                this.fullView = val
                this.$refs.datamap.resize()
            }
        },
        mounted() {
            this.$store.dispatch('loadRoadData', [this.$store.state.userInfo, 21])
            var height = document.documentElement.clientHeight - 195
            if (height >= 400) {
                this.mapstyle.height = height + "px"
            } else {
                this.mapstyle.height = "368px"
            }
            this.$nextTick(function() {
                window.addEventListener('resize', this.resizeMap)
                window.addEventListener("orientationchange", this.resizeMap)
            })
        },
        beforeDestroy() {
            window.removeEventListener('resize', this.resizeMap);
            window.removeEventListener("orientationchange", this.resizeMap)
        },
        methods: {
            resizeMap(event) {
                var height = document.getElementById("mapView").clientHeight - 30
                this.mapstyle.height = height + "px"
                this.$refs.datamap.resize()
            },
            expand() {
                this.fullView = !this.fullView;
                this.$emit('expand')
                this.$refs.datamap.resize()
            }
        },
        data() {
            return {
                fullView: false,
                options: {
                    clickableIcons: false,
                    fullscreenControl: false,
                    streetViewControl: false,
                    mapTypeControl: false,
                },
                center: {
                    lat: 40,
                    lng: -86
                },
                mapstyle: {
                    width: "100%",
                    height: "300px",
                },
                rawline1: {
                    strokeColor: '#bf4031',
                    geodesic: true,
                    strokeWeight: 3,
                },
                rawline2: {
                    strokeColor: '#ffffff',
                    geodesic: true,
                    strokeWeight: 7,
                }
            }
        },
    }

</script>

<style scoped="true">
    .toolbox {
        padding: 5px 5px 5px 5px;
        position: absolute;
        text-align: -webkit-center;
        z-index: 99;
        top: 30px;
        right: 5px;
    }
    
    .tool {
        width: 30px;
        height: 30px;
        background-color: #ffffff;
        border: 2px;
        border-radius: 2px 2px 2px 2px;
        cursor: pointer;
        box-shadow: 1px 1px 1px rgba(0, 0, 0, .1);
        color: #666666;
        transition: color 0.1s;
    }
    
    .tool:hover {
        color: #2f2f2f;
    }
    
    .fa-mouse-pointer {
        font-size: 12px;
        margin-left: 2px;
        position: relative;
        top: 2px;
    }
    
    .title {
        text-align: left;
        vertical-align: middle;
        background-color: #bf4031;
        border-radius: 3px 3px 0 0;
    }
    
    .option-icon {
        color: azure;
        margin: 4px;
        transition: color 0.1s;
        cursor: pointer;
    }
    
    .fa-map-o {
        color: azure;
        margin: 4px;
    }
    
    .option-icon:hover {
        color: #ffa098;
    }
    
    .corner-icon {
        display: inline;
        float: right;
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
    
    .expand-enter-active,
    .expand-leave-active {
        transition: opacity .15s
    }
    
    .expand-enter,
    .expand-leave-to
    /* .fade-leave-active in <2.1.8 */
    
    {
        opacity: 0
    }

</style>
