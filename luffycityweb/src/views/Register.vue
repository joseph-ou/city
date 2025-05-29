<template>
  <div class="login box">
    <img src="../assets/Loginbg.3377d0c.jpg" alt="">
    <div class="login">
      <div class="login-title">
        <img src="../assets/logo.svg" alt="">
        <p>注册页面</p>
      </div>

      <div class="login_box">
        <div class="title">
          <span class="active">用户注册</span>
        </div>

        <div class="inp">
          <input type="text" v-model="state.mobile" placeholder="手机号" class="user">
          <input type="password" v-model="state.password" placeholder="登录密码" class="user">
          <input type="password" v-model="state.re_password" placeholder="确认密码" class="user">
          <input type="code" v-model="state.code" placeholder="验证码" class="code">
          <el-button id="get_code" type="primary">获取验证码</el-button>
          <button class="login_btn">注册</button>

          <p class="go_login">已有账号 <router-link to="/login">跳转至登录</router-link></p>

        </div>


      </div>

    </div>


  </div>
</template>


<script setup>
import {reactive} from "vue";


const state=reactive({
  mobile:'',
  password:'',
  re_password:'',
  code:'',
})


</script>


<style scoped>

</style>