import Vue from 'vue'
import VueRouter from 'vue-router'
import * as VueGoogleMaps from 'vue2-google-maps'
import App from './App'
import 'bootstrap/dist/css/bootstrap.css'
import 'font-awesome/css/font-awesome.css'
import Navbar from './components/Navbar'
import Login from './components/Login'
import Home from './components/Home'
import VueResource from 'vue-resource'
import store from './store'

Vue.component('grid-loader', require('vue-spinner/src/GridLoader.vue'));
Vue.use(VueRouter)
Vue.use(VueGoogleMaps, {
        load: {
            key: 'AIzaSyDrb9lBvJ3GpVOi70FUw4dk0lAlj2TcSeM',
            v: '3', // Google Maps API version 
            // libraries: 'places',   // If you want to use places input 
        }
    })
Vue.use(VueResource)



const routes = [{
    path: '/',
    component: Login
},{
    path: '/platform',
    component: Home
}]
const router = new VueRouter( {
    routes
})

new Vue({
    router,
    store,
    ...App
}).$mount('#app')