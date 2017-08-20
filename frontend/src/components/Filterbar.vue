<template>
  <div class="card bar">
    <div class="title">
        <span class="title-text"><i class="fa fa-filter fa-lg" aria-hidden="true"></i> Filter</span>
    </div>
    
    <div class="filter">
       
        <click-outside :handler="clickOutsideDate" class="filter-btn">
            <span class="filter-btn-text" v-on:click="date.isOpened=!date.isOpened">Date</span>
            <span class="filter-text"  v-on:click="date.isOpened=!date.isOpened">{{ dateRange }}</span>
            
        <div v-if="date.isOpened" class="card popup">
            <div class="popup-title"><span class="popup-title-text">Date</span></div>
            <div class="popup-block">
                    <label class="filter-text" for="sday"><input v-on:click="date.isFrom=!date.isFrom;" class="check-input" type="checkbox" value="">       From</label>
                  <input :disabled="!date.isFrom" class="form-control filter-input-date" type="Date" name="sday">
                   <hr class="hr">
                    <label class="filter-text" for="sday"><input v-on:click="date.isTo=!date.isTo;" class="check-input" type="checkbox" value="">       To</label>
                  <input :disabled="!date.isTo" class="form-control filter-input-date" type="Date" name="sday">
            </div>
        </div>
    </click-outside>
      
      <div class="vr"></div>
        
        <click-outside :handler="clickOutsideRaw" class="filter-btn">
        <span class="filter-btn-text" v-on:click="raw.isOpened=!raw.isOpened">Index (Alpha)</span>
            <span v-if="raw.isApplied&&raw.isRange" class="filter-text" v-on:click="raw.isOpened=!raw.isOpened">from {{ raw.slider.value[0] }} to {{ raw.slider.value[1] }} m/s<sup>2</sup></span>
            <span v-if="raw.isApplied&&!raw.isRange" class="filter-text" v-on:click="raw.isOpened=!raw.isOpened">&Delta; &lt; {{ raw.slider.value }} m/s<sup>2</sup></span>
            
            <div v-if="raw.isOpened" class="card popup">
               <div class="popup-title"><span class="popup-title-text"><input v-on:click="raw.isApplied=!raw.isApplied;raw.slider.disabled=!raw.slider.disabled;" v-bind:checked="raw.isApplied" class="check-input" type="checkbox" value=""> Raw</span></div>
                <div class="popup-block">
                       <label class="filter-text" for="rawRange">
                       <input :disabled="!raw.isApplied" v-on:click="raw.isRange=true;raw.slider.value=[5,15];" class="radio-input" type="radio" name="rawFilter" id="range" value="option1" checked>       Range</label>
                       <label class="filter-text" for="rawAmp">
                       <input :disabled="!raw.isApplied" v-on:click="raw.isRange=false;raw.slider.value=15;" class="radio-input" type="radio" name="rawFilter" id="amplitude" value="option1" checked>       Change Amplituede</label>
                       <input :disabled="!raw.isApplied" v-if="raw.isRange" type= "number" min="5" :max="raw.slider.value[1]" step="0.01" class="form-control filter-input-number" v-model="raw.slider.value[0]">
                       <span v-if="raw.isRange" class="filter-text-item">to</span>
                       <input :disabled="!raw.isApplied" v-if="raw.isRange" type= "number" :min="raw.slider.value[0]" max="15" step="0.01" class="form-control filter-input-number" v-model="raw.slider.value[1]">
                       <input :disabled="!raw.isApplied" v-else type= "number" min="5" :max="15" step="0.01" class="form-control filter-input-number" v-model="raw.slider.value">
                       <vue-slider v-bind="[slider,raw.slider]" ref="rawSlider" v-model="raw.slider.value"></vue-slider>
                </div>
            </div>
       </click-outside>
       

 <!--        <div class="vr"></div>
        
        <click-outside :handler="clickOutsidePci" class="filter-btn">
        <span class="filter-btn-text" v-on:click="pci.isOpened=!pci.isOpened">PCI</span>
            <span v-if="pci.isApplied&&pci.isRange" class="filter-text" v-on:click="pci.isOpened=!raw.isOpened">from {{ pci.slider.value[0] }} to {{ pci.slider.value[1] }}</span>
            <span v-if="pci.isApplied&&!pci.isRange" class="filter-text" v-on:click="pci.isOpened=!raw.isOpened">&Delta; &lt; {{ pci.slider.value }}</span>
            
            <div v-if="pci.isOpened" class="card popup">
               <div class="popup-title"><span class="popup-title-text"><input v-on:click="pci.isApplied=!pci.isApplied;pci.slider.disabled=!pci.slider.disabled;" v-bind:checked="pci.isApplied" class="check-input" type="checkbox" value=""> PCI</span></div>
                <div class="popup-block">
                       <label class="filter-text" for="pciRange">
                       <input :disabled="!pci.isApplied" v-on:click="pci.isRange=true;pci.slider.value=[0,50];" class="radio-input" type="radio" name="pciFilter" id="range" value="option1" checked>       Range</label>
                       <label class="filter-text" for="pciAmp">
                       <input :disabled="!pci.isApplied" v-on:click="pci.isRange=false;pci.slider.value=50;" class="radio-input" type="radio" name="pciFilter" id="amplitude" value="option1" checked>       Change Amplituede</label>
                       <input :disabled="!pci.isApplied" v-if="pci.isRange" type= "number" min="0" :max="pci.slider.value[1]" class="form-control filter-input-number" v-model="pci.slider.value[0]">
                       <span v-if="pci.isRange" class="filter-text-item">to</span>
                       <input :disabled="!pci.isApplied" v-if="pci.isRange" type= "number" :min="pci.slider.value[0]" max="100" class="form-control filter-input-number" v-model="pci.slider.value[1]">
                       <input :disabled="!pci.isApplied" v-else type= "number" min="0" :max="100" class="form-control filter-input-number" v-model="pci.slider.value">
                       <vue-slider v-bind="[slider,pci.slider]" ref="pciSlider" v-model="pci.slider.value"></vue-slider>
                </div>
            </div>
        </click-outside>-->

    
    <div class="export">
        <span class="title-text">Export <i class="fa fa-download fa-lg" aria-hidden="true"></i></span>
    </div>
    </div>
  </div>
</template>




<script>
    import vueSlider from 'vue-slider-component'
    import ClickOutside from 'onclick-outside'

    export default {
        components: {
            vueSlider,
            ClickOutside
        },
        mounted() {

        },
        beforeDestroy() {

        },
        methods: {
            clickOutsideRaw(e) {
                this.raw.isOpened = false;
            },
//            clickOutsidePci(e) {
//                this.pci.isOpened = false;
//            }
        },
        data() {
            return {
                dateRange: "",
                filterData: {
                    startTime: "",
                    endTime: "",
                    raw: "",
//                    pci: "",
                },
                slider: {
                    tooltip: 'disable',
                        clickable: true,
                        tooltipDir: 'bottom',
                        piecewise: false,
                        lazy: false,
                        speed: 0.5,
                        formatter: null,
                        sliderStyle: null,
                        bgStyle: {
                            "backgroundColor": "#fff",
                            "boxShadow": "inset 0.5px 0.5px 3px 1px rgba(0,0,0,.1)"
                        },
                        tooltipStyle: {
                            "backgroundColor": "#F5F5F5",
                            "borderColor": "#bdbdbd",
                            "color": "black"
                        },
                        processStyle: {
                            "backgroundColor": "#bf4031"
                        },
                        piecewiseStyle: null
                },
                date: {
                    isOpened: false,
                    isFrom:false,
                    isTo:false,
                    isApplied: false,
                    dateFrom:"",
                    dateTo:"",
                },
                raw:{
                    isApplied: false,
                    isOpened: false,
                    isRange: false,
                    slider: {
                        value: 10,
                        width: 200,
                        min: 5,
                        max: 15,
                        interval: 0.01,
                        disabled: true,
                    },
                },
//                pci: {
//                    isApplied: false,
//                    isOpened: false,
//                    isRange: false,
//                    slider: {
//                        value: 50,
//                        width: 200,
//                        min: 0,
//                        max: 100,
//                        interval: 1,
//                        disabled: true,
//                    },
//                }
            }
        },
    }

</script>

<style scoped="true">
    div.popup {
        position: fixed;
        z-index: 100;
        width: auto;
        height: auto;
        top: 130px;
    }
    
    .title {
        float: left;
        background-color: #bf4031;
        border-radius: 3px 0px 0px 3px;
        height: 100%;
        display: table;
    }
    
    .export {
        float: right;
        background-color: #bf4031;
        transition: background-color 0.3s;
        border-radius: 0 3px 3px 0;
        height: 100%;
        display: table;
        cursor: pointer;
    }
    
    .export:hover {
        background-color: #99291b;
    }
    
    .filter {
        float: left;
        height: 100%;
        display: table;
    }
    
    .filter-btn {
        float: left;
        line-height: 33px;
        display: flex;
        white-space: nowrap;
        margin: 0;
        cursor: pointer;
        background-color: #F5F5F5;
        transition: background-color 0.3s;
    }
    
    .filter-btn:hover {
        background-color: #bdbdbd;
    }
    
    .filter-btn:hover span.filter-btn-text {
        color: #F5F5F5;
    }
    
    .vr {
        padding: 0;
        float: left;
        height: 33px;
        background-color: #d8d8d8;
        width: 1px;
    }
    
    .hr {
        margin: 1px;
    }
    
    .filter-item {
        float: left;
        line-height: 33px;
        display: flex;
        white-space: nowrap;
    }
    
    .filter-input-date {
        height: 33px;
        font-size: 0.8em;
        font-family: Helvetica Neue;
        font-weight: 200;
        margin: 0 0 8px 0;
        border: 0;
        padding: 0 0 0 5px;
    }
    
    .filter-input-number {
        height: 33px;
        font-size: 0.8em;
        font-family: Helvetica Neue;
        font-weight: 200;
        margin: 0 0 8px 0;
        border: 0;
        padding: 0 0 0 5px;
        display: inline;
        width: 90px;
    }
    
    .title-text {
        font-family: Helvetica Neue;
        font-weight: 200;
        font-size: 0.8em;
        color: azure;
        padding: 0 5px 0 5px;
        display: table-cell;
        vertical-align: middle;
        transition: color 0.3s;
    }
    
    .filter-text {
        font-family: Helvetica Neue;
        font-weight: 400;
        font-size: 0.8em;
        color: #000000;
        padding: 0 5px 0 5px;
        display: table-cell;
    }
    
    .filter-text-item {
        font-family: Helvetica Neue;
        font-weight: 400;
        font-size: 0.8em;
        color: #78828b;
    }
    
    .filter-btn-text {
        font-family: Helvetica Neue;
        font-weight: 400;
        font-size: 0.8em;
        padding: 0 5px 0 5px;
        color: #8b97a2
    }
    
    .card {
        background-color: #d8d8d8;
        height: 35px;
        box-shadow: 1px 1px 2px rgba(0, 0, 0, .3);
    }
    
    label {
        display: inline-block;
        height: 100%;
        vertical-align: middle;
        margin: 0;
    }
    
    .popup-title {
        text-align: left;
        background-color: #bf4031;
        border-radius: 3px 3px 0 0;
        height: 24px;
    }
    
    .popup-title-text {
        font-family: Helvetica Neue;
        font-weight: 200;
        font-size: 0.8em;
        color: azure;
        margin: 4px 0 4px 4px;
        position: absolute;
        line-height: 18px;
    }
    
    .popup-block {
        margin: 5px 5px 5px 5px;
    }
    
    .bar {
        margin-bottom: 0;
    }

</style>
