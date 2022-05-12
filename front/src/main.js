import { createApp } from 'vue'
import App from './App.vue'
import Vant from 'vant';
import { Lazyload } from 'vant' // 导入懒加载模块Lazyload
import 'vant/lib/index.css';
import router from "@/router/router";

const app = createApp(App);
app.use(Vant);
app.use(Lazyload)
app.use(router)

app.mount('#app')

const user=localStorage.getItem("user")
if(user!==null){
    app.config.globalProperties.$user=JSON.parse(user)
}else{
    router.push("/login")
}
