import httpRequest from '@/request/index'
import {getFormData} from "@/utils/formDataUtil"

const path = '/user/'

export function apiUserLogin(param) {
    return httpRequest({
            url: path + 'login/',
            method: 'POST',
            data: getFormData(param)
        })
}

export function apiUserRegister(param) {
    return httpRequest({
        url: path + 'register/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiUserBindPhone(param) {
    return httpRequest({
        url: path + 'bindPhone/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiUserBindEmail(param) {
    return httpRequest({
        url: path + 'bindEmail/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiUserUpdate(param) {
    return httpRequest({
        url: path + 'update/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiUserChangePassword(param) {
    return httpRequest({
        url: path + 'changePassword/',
        method: 'POST',
        data: getFormData(param)
    })
}