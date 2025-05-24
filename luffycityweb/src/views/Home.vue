<template>

    <div class="home">
      <Header></Header>


      <Footer></Footer>
    </div>
</template>

<script setup>
import {reactive} from 'vue';
import Header from  '../components/Header.vue'
import Footer from  '../components/Footer.vue'


//测试cors的跨域配置是否有问题
// import axios  from "axios";
// const http=axios.create()
//
// //测试服务端的跨域是否配置成功 get post put
// http.get('http://api.luffycity.cn:8000/home/test').then(res=>{
//   console.log(res.data)
// })

import http from '../utils/http.js'
http.get('/home/test').then(res=>{
  console.log(res.data)
})


    const store=reactive({
      value2:null,
      colors:['#99A98F','#F7BA2A','#FF9900'],
    })
</script>

<style scoped>

</style>