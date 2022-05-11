// 导入axios实例
import httpRequest from '@/request/index'
import {getFormData} from "@/utils/formDataUtil";


// 定义接口的传参
// interface UserInfoParam {
//     userID: string,
//     userName: string
// }

// 获取用户信息
export function apiGetUserInfo(param) {
    return httpRequest({
        url: 'http://127.0.0.1:8000/manga/getMangaChapterImages/',
        method: 'POST',
        // data: {
        //     "chapter_url": "http://www.ykmh.com/manhua/kexuecunzaiderenwainiangguanchariji/34754.html",
        //     "cookie": localStorage.getItem("cookie")
        // }
        data: getFormData(param)
    })
}
