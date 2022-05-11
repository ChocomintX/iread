import axios from 'axios'

// 创建一个 axios 实例
const service = axios.create({
    // baseURL: 'http://10.91.11.58:8000/', // 所有的请求地址前缀部分
    // baseURL: 'http://172.20.10.2:8000/',
    // baseURL: 'http://42.193.223.241:6001/',
    baseURL: 'http://localhost:8000/',
    timeout: 60000, // 请求超时时间毫秒
    withCredentials: true, // 异步请求携带cookie
    headers: {
        // 设置后端需要的传参类型
        'Content-Type': 'multipart/form-data',
        // 'token': 'your token',
        // 'X-Requested-With': 'XMLHttpRequest',
    },
})

// 添加请求拦截器
service.interceptors.request.use(
    function (config) {
        // 在发送请求之前做些什么
        return config
    },
    function (error) {
        // 对请求错误做些什么
        console.log(error)
        return Promise.reject(error)
    }
)

// 添加响应拦截器
service.interceptors.response.use(
    function (response) {
        // console.log(response)
        // 2xx 范围内的状态码都会触发该函数。
        // 对响应数据做点什么
        // dataAxios 是 axios 返回数据中的 data
        const dataAxios = response.data
        // 这个状态码是和后端约定的
        const code = dataAxios.code
        const msg = dataAxios.msg
        const error_msg = dataAxios.error_msg
        if(code===0)
            console.log(msg)
        else
            console.log(error_msg)
        return dataAxios
    },
    function (error) {
        // 超出 2xx 范围的状态码都会触发该函数。
        // 对响应错误做点什么
        console.log(error)
        return Promise.reject(error)
    }
)

export default service

