<!--登陆用组件-->
<template>
  <div class="title">
    <span :class="{active:user.login_type==0}" @click="user.login_type=0">密码登录</span>
    <span :class="{active:user.login_type==1}" @click="user.login_type=1">短信登录</span>
  </div>
  <div class="inp" v-if="user.login_type==0">
    <input v-model="user.username" type="text" placeholder="用户名 / 手机号码" class="user">
    <input v-model="user.password" type="password" class="pwd" placeholder="密码">
    <div id="geetest1"></div>
    <div class="rember">
      <label>
        <input v-model="user.remember" type="checkbox" class="no" name="a"/>
        <span >记住密码</span>
      </label>
      <p>忘记密码</p>
    </div>
    <button class="login_btn" @click="show_captcha">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
  <div class="inp" v-show="user.login_type==1">
    <input v-model="user.mobile" type="text" placeholder="手机号码" class="user">
    <input v-model="user.code"  type="text" class="code" placeholder="短信验证码">
    <el-button id="get_code" type="primary">获取验证码</el-button>
    <button class="login_btn">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
</template>

<script setup>
import {useStore} from "vuex";
import {reactive} from "vue";
import user from '../api/user.js'//标准化登录用户信息并发送

import '../utils/TCaptcha.js'
import {ElMessage} from "element-plus";//发送提示框

// 用 const emit = defineEmits(['事件名']) 定义子组件可能触发的事件
const emit = defineEmits(["successhandle",])

//引入vuex的store记录登录信息
const store=useStore()

//显示登录验证码
const show_captcha=()=>{
    var captcha1 = new TencentCaptcha('192768512', (res)=>{
      // 接收验证结果的回调函数
      /* res（验证成功） = {ret: 0, ticket: "String", randstr: "String"}
         res（客户端出现异常错误 仍返回可用票据） = {ret: 0, ticket: "String", randstr: "String", errorCode: Number, errorMessage: "String"}
         res（用户主动关闭验证码）= {ret: 2}
      */
      console.log(res);
      // 调用登录处理
      loginhandeler(res);
    });
  captcha1.show(); // 显示验证码
}


//前端进行提交验证
const loginhandeler=(res)=>{
  if(user.username.length<1 || user.password.length<1){
    console.log('账号或密码为空,登录失败');
    ElMessage.error('账号或密码为空,登录失败');
    return;
  }

  //登录处理
  user.login({
      ticket:res.ticket,
      randstr:res.randstr
  }).then(res=>{
    // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("access");
    sessionStorage.removeItem("access");

    if(user.remember){ // 判断是否记住登录状态
      // 记住登录
      localStorage.access = res.data.access
    }else{
      // 不记住登录，关闭浏览器以后就删除状态
      sessionStorage.access = res.data.access
    }
    // 保存token，并根据用户的选择，是否记住密码
    // 成功提示

    // console.log(res.data.access)
    ElMessage.success('登录成功 跳转中')
    // vuex存储用户登录信息，保存token，并根据用户的选择，是否记住密码
    let payload = res.data.access.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    console.log(payload_data)
    store.commit("login", payload_data)


    //关闭弹窗 并且使用emit通知父组建关闭登录弹窗 或者跳转
    //emit 有两种写法：
    // Options API：用 this.$emit('事件名', 数据)。
    // Composition API（<script setup>）：用 defineEmits 定义事件，再用 emit('事件名', 数据)。
    user.username='';
    user.login_type=0;
    user.password='';
    user.code='';
    user.remember=false;
    emit('successhandle')

  }).catch(err => {
    ElMessage.error(err)
  })

}





</script>

<style scoped>
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
    border-bottom: 2px solid #84cc39;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp .code{
    width: 220px;
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