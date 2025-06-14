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
          <input type="text" v-model="user.mobile" placeholder="手机号" class="user">
          <input type="password" v-model="user.password" placeholder="登录密码" class="user">
          <input type="password" v-model="user.re_password" placeholder="确认密码" class="user">
          <input type="code" v-model="user.code" placeholder="验证码" class="code">
          <el-button id="get_code" type="primary">获取验证码</el-button>
          <button class="login_btn" @click="show_captcha">注册</button>

          <p class="go_login">已有账号 <router-link to="/login">跳转至登录</router-link></p>

        </div>


      </div>

    </div>


  </div>
</template>


<script setup>

import {reactive, defineEmits,watch} from "vue"

import {useStore} from "vuex"
import user from '@/api/user.js'
import {ElMessage} from "element-plus";//发送提示框

import "../utils/TCaptcha"
import settings from "@/settings.js";

const store=useStore()

//引入user记录 效果如下
// const state=reactive({
//   mobile:'',
//   password:'',
//   re_password:'',
//   code:'',
// })

// 监测手机号是否存在
//前端检测手机号格式是否正确
watch(()=>user.mobile,(mobile,prev_mobile)=>{
  //第一个箭头函数代表watch检测的值，第二个是回调函数
  if(/1[3-9]\d{9}/.test(user.mobile)){
    //发送请求看手机号是否注册 test是正则匹配
    user.check_mobile().then(res=>{
      ElMessage.success('手机号可注册')
    }).catch(err=>{
      console.log(err)
      ElMessage.error(err.response.data.msg);
    })
  }

});

// 显示登录验证码
const show_captcha = ()=>{
  // 直接生成一个验证码对象
  let  captcha1 = new TencentCaptcha(settings.captcha_app_id, (res)=>{
    // 验证码通过验证以后的回调方法
    if(res && res.ret === 0){
      // 验证通过，发送登录请求
      registerhandler(res)
    }
  });

  // 显示验证码
  captcha1.show();
}

const registerhandler = (res)=> {
  // 注册处理
  if (!/^1[3-9]\d{9}$/.test(user.mobile)) {
    // 错误提示
    ElMessage.error('手机号格式不正确！');
    return false // 阻止代码继续往下执行
  }
  if (user.password.length < 6 || user.password.length > 16) {
    ElMessage.error('密码必须在6~16个字符之间！');
    return false
  }

  if (user.password !== user.re_password) {
    ElMessage.error('密码和确认密码不一致！');
    return false
  }

    // 发送请求
  user.register({
    // 验证码通过的票据信息
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(response=>{
    // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("access");
    sessionStorage.removeItem("access");

    // 默认不需要记住登录
    sessionStorage.access = response.data.access;

    // vuex存储用户登录信息
    let payload = response.data.access.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    store.commit("login", payload_data)
    // 清空表单信息
    user.mobile = ""
    user.password = ""
    user.code = ""
    user.remember = false
    //  成功提示
    ElMessage.success("注册成功！");
    // 路由跳转到首页
    router.push("/");


  })
}



</script>


<style scoped>
.box{
	width: 100%;
  height: 100%;
	position: relative;
  overflow: hidden;
}
.box img{
	width: 100%;
  min-height: 100%;
}
.box .login {
	position: absolute;
	width: 500px;
	height: 400px;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -438px;
}

.login-title{
     width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.login_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
    padding-top: 50px;
}
.title{
	font-size: 20px;
	color: #9b9b9b;
	letter-spacing: .32px;
	border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 0px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}
.title span.active{
	color: #4a4a4a;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp .code{
  width: 190px;
  margin-right: 16px;
}
#get_code{
 margin-top: 6px;
}
.inp input{
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
     display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
    vertical-align: middle;
    margin-right: 4px;
}

.inp .rember p span{
    display: inline-block;
  font-size: 12px;
  width: 100px;
}
.login_btn{
    cursor: pointer;
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
    border: none;
    outline: none;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>