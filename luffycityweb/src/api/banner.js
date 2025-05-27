import http from '../utils/http.js'
import {reactive,ref} from "vue";

const banner=reactive({
    banner_list:[],

    get_banner_img(){
    //获取轮播图
       return  http.get('/home/banner')

    },
})


export default banner