<template>
  <div>
  <div class="navbar">
   <navbar></navbar>
   </div>
    <div class="container" style="width:100%;height: 100%;padding: 0;">
        <div class="info hidden-sm-down" id="info">
            <info></info>
            <transition name="fade">
            <span  v-if="this.$store.state.firstTime" class="prompt">First time user?<br>Please fill in your vehicle infomation.</span>
            </transition>
        </div>
        <div class="container data-container" id="dataContainer">
            <div class="filter">
                <filterbar></filterbar>
            </div>
            <div v-show="!fullRight" class="data" v-bind:style="dataLeft" id="dataLeft">
                <keep-alive>
                    <component :is="viewLeft" @switch="switchView(true)" @expand="expandLeft" v-bind:expanded="fullLeft">
                    </component>
                </keep-alive>
            </div>
            <div v-if="!(fullRight|fullLeft)" class="divider" v-bind:style="divider" id="divider">
               <div class="divider-icon" draggable="false" @mousedown="resizeStart" @touchstart="resizeStart" @mouseup="resizeEnd" @touchend="resizeEnd">
                <div class="divider-line divider-line-2"></div>
                <div class="divider-line"></div>
                <div class="divider-line divider-line-2"></div>
                </div>
            </div>
            <div v-show="!fullLeft" class="data" v-bind:style="dataRight" id="dataRight">
                <keep-alive>
                    <component :is="viewRight" @switch="switchView(false)" @expand="expandRight" v-bind:expanded="fullRight">
                    </component>
                </keep-alive>
            </div>
        </div> 
    </div>
    <transition name="fade">
    <div v-if="this.$store.state.firstTime" class="fade-out"></div>
    </transition>
  </div>
</template>




<script>
    import Navbar from './Navbar'
    import Info from './Info'
    import Filterbar from './Filterbar'
    import Maps from './Maps'
    import Statics from './Statics'
    import Plot from './Plot'
    export default {
        components: {
            Navbar,
            Info,
            Filterbar,
            Maps,
            Statics,
            Plot,
        },
        created() {
            
        },
        mounted() {
            this.dataChangeView();
            this.$nextTick(function() {
                window.addEventListener('resize', this.dataChangeView)
                window.addEventListener('mouseup', this.resizeEnd, true);
            })
        },
        beforeDestroy() {
            window.removeEventListener('resize', this.dataChangeView);
            this.$store.dispatch('loading', false);
        },
        methods: {
            switchView(isLeft) {
                for (var view in this.views) {
                    if (this.views[view] != this.viewLeft && this.views[view] != this.viewRight) break
                }
                if (isLeft) {
                    this.viewLeft = this.views[view]
                } else {
                    this.viewRight = this.views[view]
                }
            },
            dataChangeView(event) {
                var width = document.documentElement.clientWidth

                var height = document.documentElement.clientHeight - 165
                if (height >= 300) {
                    this.dataLeft.height = height + "px"
                    this.dataRight.height = height + "px"
                    this.divider.height = height + "px"
                } else {
                    this.dataLeft.height = "400px"
                    this.dataRight.height = "400px"
                    this.divider.height = "400px"
                }
            },
            resizeEnd(e) {
                window.removeEventListener('mousemove', this.resize, true);
                window.removeEventListener('touchmove', this.resize, true);
            },
            resizeStart(e) {
                window.addEventListener('mousemove', this.resize, true);
                window.addEventListener('touchmove', this.resize, true);
            },
            resize(e) {
                e.preventDefault()
                var mousePos = e.clientX
                var offset = document.getElementById("info").clientWidth
                var width = document.documentElement.clientWidth
                var left = (mousePos - offset - 58) / (width - offset - 100)
                if (left > 0.8) {
                    this.fullLeft = true
                    this.fullRight = false
                    this.dataLeft.width = 100 + "%"
                } else if (left < 0.2) {
                    this.fullRight = true
                    this.fullLeft = false
                    this.dataRight.width = 100 + "%"
                } else {
                    this.fullRight = false
                    this.fullLeft = false
                    this.dataLeft.width = left * 100 + "%"
                    this.dataRight.width = (98 - left * 100) + "%"
                    this.lastDivider = left * 100
                }

            },
            expandLeft() {
                if (this.fullLeft) {
                    this.fullLeft = false
                    this.dataLeft.width = this.lastDivider + "%"
                    this.dataRight.width = (98 - this.lastDivider) + "%"
                } else {
                    this.fullLeft = true
                    this.fullRight = false
                    this.dataLeft.width = 100 + "%"
                }
            },
            expandRight() {
                if (this.fullRight) {
                    this.fullRight = false
                    this.dataLeft.width = this.lastDivider + "%"
                    this.dataRight.width = (98 - this.lastDivider) + "%"
                } else {
                    this.fullRight = true
                    this.fullLeft = false
                    this.dataRight.width = 100 + "%"
                }
            },
        },
        data() {
            return {
                views: ['statics', 'maps', 'plot'],
                viewLeft: 'statics',
                viewRight: 'maps',
                lastDivider: 49,
                fullLeft: false,
                fullRight: false,
                dataLeft: {
                    height: "300px",
                    width: "49%",
                },
                dataRight: {
                    height: "300px",
                    width: "49%",
                },
                divider: {
                    height: "300px",
                }
            }
        },
    }

</script>

<style scoped="true">
    .prompt {
        position: absolute;
        color: aliceblue;
        font-family: Helvetica Neue;
        font-weight: 200;
        left: 110%;
        top: 240px;
        z-index: 200;
        width: 300px;
    }
    
    .fade-out {
        position: fixed;
        height: 100%;
        width: 100%;
        top: 0px;
        left: 0px;
        z-index: 199;
        background-color: black;
        opacity: 0.5;
    }
    
    div.divider-line {
        background-color: #cfd8db;
        position: relative;
        width: 2px;
        height: 20px;
        position: relative;
        float: left;
        margin-left: 1px;
        border-radius: 1px 1px 1px 1px;
        transition: background-color 0.2s;
    }
    
    div.divider-icon:hover div {
        background-color: #8d8d8d;
    }
    
    div.divider-line-2 {
        height: 10px;
        top: 5px;
    }
    
    div.divider-icon {
        height: 20px;
        width: 100%;
        position: relative;
        top: 50%;
        margin-top: -10px;
        left: 50%;
        margin-left: -5px;
        cursor: col-resize;
    }
    
    div.divider {
        position: relative;
        width: 2%;
        margin-top: 20px;
        float: left;
    }
    
    div.data {
        position: relative;
        margin-top: 20px;
        float: left;
    }
    
    div.navbar {
        width: 100%;
        padding: 0;
    }
    
    div.info {
        float: left;
        width: 16.66%;
        min-width: 192px;
        max-width: 220px;
        height: 100%;
        padding: 20px 0px 20px 20px;
        position: relative;
        z-index: 10000;
    }
    
    div.data-container {
        width: auto;
        height: 100%;
        padding: 0;
        overflow: hidden;
        padding: 20px 40px 20px 40px;
    }
    
    div.filter {
        height: 35px;
    }
    
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity .5s
    }
    
    .fade-enter,
    .fade-leave-to
    /* .fade-leave-active below version 2.1.8 */
    
    {
        opacity: 0
    }

</style>
