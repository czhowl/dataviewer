<template>
   <div class="card" id="mapView">
       <div class="title"><i class="fa fa-line-chart" aria-hidden="true"></i><span class="option-text">Plot</span><div class="corner-icon"><i class="fa fa-exchange option-icon" title="change view" aria-hidden="true" @click="$emit('switch')"></i>
       <transition name="expand" mode="out-in">
       <i v-if="!fullView" class="fa fa-expand option-icon" title="Maximize" key="max" aria-hidden="true" @click="expand"></i>
       <i v-else class="fa fa-compress option-icon" title="Minimize" key="min" aria-hidden="true" @click="expand"></i>
       </transition>
    </div></div>
    
    </div>
</template>

<script>
    export default {
        props: {
            expanded: {
                type: Boolean,
                default: false,
            }
        },
        watch: {
            expanded: function(val) {
                this.fullView = val
            }
        },
        mounted() {},
        beforeDestroy() {},
        methods: {
            expand() {
                this.fullView = !this.fullView;
                this.$emit('expand')
            }
        },
        data() {
            return {
                fullView: false,
            }
        },
    }

</script>

<style scoped="true">
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
    
    .fa-line-chart {
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
