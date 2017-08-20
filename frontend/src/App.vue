<template>
  <div id="app">
     <transition name="fade" mode="out-in">
    <login v-if="!this.$store.state.logIn"></login>
    <home v-else></home>
  </transition>
      
      </div>
      
</template>

<script>
    import Login from './components/Login'
    import Home from './components/Home'
    export default {
        name: 'app',
        created() {

            this.$http.get('/api/relogin').then((response) => {
                // has logged in
                var jsondata = response.body;
                if (jsondata.hasOwnProperty('authentication_token') && jsondata.hasOwnProperty('username')) {
                    this.$store.dispatch('logInUser', jsondata)
                    
                } else {
                    this.$store.dispatch('loading', false);
                }
            })
        },
        mounted() {

        },
        components: {
            Login,
            Home,
        },
        data() {
            return {}
        }
    }

</script>

<style>
    .fade-enter-active {
        transition: all .1s ease-in-out;
    }
    
    .fade-leave-active {
        transition: all .3s ease-in-out;
    }
    
    .fade-enter,
    .fade-leave-to
    /* .slide-fade-leave-active for <2.1.8 */
    
    {
        transform: translateY(-1000px);
    }

</style>
