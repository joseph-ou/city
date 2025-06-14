import http from '../utils/http.js'
import {reactive,ref} from "vue";

const user=reactive({
    login_type:0,//登录方式
    username:'',//登录账号/手机号/邮箱
    password:'',//密码
    remember:false,//登录状态

    mobile:'',//手机号 登录/注册用
    re_password:'',//再确认手机号 注册用
    code:'',//短信验证码

    login(res){
        //用户登录 发送axios请求
        return http.post('/users/login/',{
            //验证码所需
            "ticket": res.ticket,
            "randstr": res.randstr,

            "username":this.username,
            "password":this.password,
        })
    },

    check_mobile(){
        //通过前端格式检查后向后端发送请求获取手机号是否存在的信息
        return http.get(`/users/mobile/${this.mobile}/`)
    },

     register(data){
        data.mobile = this.mobile
        data.re_password = this.re_password
        data.password = this.password
        data.sms_code = this.code
        // 用户注册请求
        return http.post("/users/register/", data)
    }


})

export default user;