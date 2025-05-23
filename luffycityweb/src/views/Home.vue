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


    const store=reactive({
      value2:null,
      colors:['#99A98F','#F7BA2A','#FF9900'],
    })
</script>

<style scoped>

</style>