import http from '../utils/http.js'
import {reactive,ref} from "vue";

const user=reactive({
    login_type:0,//登录方式
    username:'',//登录账号/手机号/邮箱
    password:'',//密码
    remember:false,//登录状态
    mobile:'',//手机号
    code:'',//短信验证码

    login(){
        //用户登录 发送axios请求
        return http.post('/users/login/',{
            "username":this.username,
            "password":this.password,
        })
    },


})

export default user;