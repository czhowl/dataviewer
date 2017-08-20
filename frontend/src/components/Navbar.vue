<template>
 <click-outside :handler="handleClickOutside">
  <nav v-bind:style="{height:navHeight}">
  <div class="background">
      <a class="logo" href="#">NVH DataViewer</a>
      <img src="static/img/bar.png" class="" alt="Responsive image">
  </div>
  <div>
  <div class="status" title="Server Status">
       
        <div v-on:mouseover="showStatus=true;" v-on:mouseleave="showStatus=false;">
         <transition name="status" mode="out-in">
              <grid-loader v-if="this.$store.state.loading" :loading="loader.loading" :color="loader.color" :size="loader.size" class="loading-icon"></grid-loader>
              <i v-else class="fa fa-check-circle fa-lg ready-icon" aria-hidden="true" style="color:azure;"></i>
          </transition>
          </div>
          <transition name="status-word">
              <span v-show="showStatus" style="width: 100%; color:azure; font-family: Helvetica Neue;font-weight: 100; position:absolute; top: 25px; left: 30px; display:inline;">{{ this.$store.state.status }}</span>
          </transition>
  </div>
    <div >
       <div v-if="!collapseMenu">
        <ul class="options">
        <li class="btn">
            <div class="nav-link"><input ref="getFile" accept="text/csv" type="file" style="visibility:hidden"  multiple @change="upload"><i class="fa fa-upload fa-lg option" aria-hidden="true" title="Sync/Upload data" @click="$refs.getFile.click()"></i></div>
          </li>
         <li class="btn">
            <router-link to="" class="nav-link"><i class="fa fa-question-circle fa-lg option" aria-hidden="true" title="Help"></i></router-link>
          </li>
          <li class="btn">
            <div class="nav-link"><i class="fa fa-envelope fa-lg option" aria-hidden="true" title="Message" ></i></div>
          </li>
          <li class="btn">
            <div class="nav-link"><i class="fa fa-sign-out fa-lg option" aria-hidden="true" title="Log out" @click="logout()"></i></div>
          </li>
        </ul>
        </div>
        <div v-else>
            <i v-on:click="openMenu" id="collapsedMenu" class="fa fa-bars fa-lg option" aria-hidden="true"></i>
            <transition name="slide-down">
            <div v-if="menuOpened" class="dropdown">
              <div class="dropdown-options"><router-link to="/" class="nav-link"><i class="fa fa-upload fa-lg option" aria-hidden="true" title="sync/upload"></i><span class="dropdown-text">Sync/Upload</span></router-link></div>
               <hr>
               <div class="dropdown-options"><router-link to="/" class="nav-link"><i class="fa fa-info-circle fa-lg option" aria-hidden="true" title="information"></i><span class="dropdown-text">Information</span></router-link></div>
               <hr>
                <div class="dropdown-options"><router-link to="" class="nav-link"><i class="fa fa-question-circle fa-lg option" aria-hidden="true" title="help"></i><span class="dropdown-text">Help</span></router-link></div>
                <hr>
                <div class="dropdown-options"><i class="fa fa-envelope fa-lg option" aria-hidden="true" title="message" ></i>  <span class="dropdown-text">Message</span></div>
                <hr>
                <div class="dropdown-options"><i class="fa fa-sign-out fa-lg option" aria-hidden="true" title="log out"></i><span class="dropdown-text">Log Out</span></div>
            </div></transition>
        </div>
        </div>
        
        
    
</div>
 
  </nav>
    </click-outside>
</template>


<script>
    import ClickOutside from 'onclick-outside'
    export default {
        components: {
            ClickOutside
        },
        mounted() {
            this.collapseMenu = document.documentElement.clientWidth < 768 ? true : false
            this.$nextTick(function() {
                window.addEventListener('resize', this.collapse)
            })
        },
        beforeDestroy() {
            window.removeEventListener('resize', this.collapse);
        },
        methods: {
            upload() {
                this.$store.dispatch('loading', true);
                var formData = new FormData();
                formData.append('email',this.$store.state.userInfo.username)
                for(var i = 0; i < this.$refs.getFile.files.length; i++){
                    formData.append(this.$refs.getFile.files[i].name,this.$refs.getFile.files[i])
                }
                this.$http.post('/api/upload-data',
                    //body
                    formData,
                    //options
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data',
                            'Authentication-Token': this.$store.state.userInfo.token
                        }
                    }).then((response) => {
                    // success
                    var data = response.body
                    this.$store.dispatch('updateLastSync', data.lastSync)
                    this.$store.dispatch('loading', false);
                }, (response) => {
                    // error
                    alert('error！ ' + JSON.stringify(response))
                    if (response.status == 401) {
                        alert('timeout, please login again');
                        this.$store.dispatch('logOutUser')
                    }
                });
            },
            logout: function() {
                this.$http.get('/logout').then((response) => {
                    // 响应成功回调
                    this.$store.dispatch('logOutUser')
                    window.localStorage.removeItem("user")
                }, (response) => {
                    // 响应错误回调
                    alert('Logout出错了！ ' + JSON.stringify(response))
                });
            },
            handleClickOutside(e) {
                if (this.menuOpened) {
                    this.openMenu()
                }
            },
            collapse(event) {
                this.collapseMenu = document.documentElement.clientWidth < 768 ? true : false
                if (document.documentElement.clientWidth > 768) {
                    this.menuOpened = false
                    this.navHeight = "70px"
                }
            },
            openMenu: function() {
                var that = this
                this.menuOpening = true
                var menuIcon = document.getElementById("collapsedMenu")
                var deg = this.menuOpened ? 0 : 90
                var currDeg = this.menuOpened ? 90 : 0
                var id = setInterval(frame, 1)
                if (!that.menuOpened) {
                    that.navHeight = "270px"
                } else {
                    that.navHeight = "70px"
                }

                function frame() {
                    if (currDeg == deg) {
                        clearInterval(id);
                    } else {
                        if (that.menuOpened) {
                            currDeg += 5
                            menuIcon.style.transform = 'rotate(' + currDeg + 'deg)'
                        } else {
                            currDeg -= 5
                            menuIcon.style.transform = 'rotate(' + currDeg + 'deg)'
                        }
                    }
                }
                that.menuOpened = !that.menuOpened

            }


        },
        data() {
            return {
                navHeight: "70px",
                menuOpening: false,
                menuOpened: false,
                status: "loading data",
                showStatus: false,
                collapseMenu: true,
                loading: true,
                loader: {
                    color: "azure",
                    size: "3px",
                    loading: true,
                },

            }
        },
    }

</script>

<style scoped="true">
    * {
        margin: 0;
        padding: 0;
    }
    
    .background {
        position: absolute;
        z-index: 2;
        width: 100%;
        height: 70px;
        overflow: hidden;
        box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
    }
    
    .top-foto>img {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        display: block;
    }
    
    .logo {
        font-family: Helvetica Neue;
        font-weight: 100;
        font-size: 2em;
        color: azure;
        text-align: center;
        left: 10px;
        top: 10px;
        text-decoration: none;
        position: absolute;
    }
    
    ul li {
        display: inline;
    }
    
    .options {
        position: absolute;
        right: 50px;
        top: 22px;
        z-index: 3;
    }
    
    .btn {
        margin-left: 40px;
    }
    
    i.option {
        color: azure;
        transition: color 0.1s;
        /*        transition-timing-function: ease-in;*/
    }
    
    i.option:hover {
        color: #ffa098;
    }
    
    .status {
        position: absolute;
        left: 230px;
        height: 70px;
        width: 110px;
        z-index: 100;
    }
    
    .status-enter-active {
        transition: all .3s ease;
    }
    
    .status-leave-active {
        transition: all .3s ease;
    }
    
    .status-enter,
    .status-leave-to
    /* .slide-fade-leave-active for <2.1.8 */
    
    {
        transform: scale(0);
        opacity: 0;
    }
    
    .loading-icon {
        position: absolute;
        top: 26px;
    }
    
    .ready-icon {
        position: absolute;
        top: 29px;
    }
    
    .status-word-enter-active {
        transition: all .3s ease;
    }
    
    .status-word-leave-active {
        transition: all .8s ease;
    }
    
    .status-word-enter,
    .status-word-leave-to
    /* .slide-fade-leave-active for <2.1.8 */
    
    {
        transform: translateX(-10px);
        opacity: 0;
    }
    
    #collapsedMenu {
        top: 29px;
        right: 30px;
        position: absolute;
        z-index: 3;
    }
    
    .dropdown {
        width: 100%;
        top: 70px;
        position: relative;
        z-index: 1;
        text-align: center;
        vertical-align: middle;
        line-height: 40px;
    }
    
    .dropdown-text {
        font-family: Helvetica Neue;
        font-weight: 100;
        font-size: 1em;
        color: azure;
        margin-left: 10px;
    }
    
    div.dropdown-options {
        height: 40px;
        background-color: #99291b;
        transition: background-color 0.3s
    }
    
    div.dropdown-options:hover {
        background-color: #c75d50;
    }
    
    .slide-down-enter-active {
        transition: all .2s ease-in;
    }
    
    .slide-down-leave-active {
        transition: all .2s ease-in;
    }
    
    .slide-down-enter,
    .slide-down-leave-to
    /* .slide-fade-leave-active for <2.1.8 */
    
    {
        transform: translateY(-200px);
    }

</style>
