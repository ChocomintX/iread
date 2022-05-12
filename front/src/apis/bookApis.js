import {getFormData} from "@/utils/formDataUtil"
import httpRequest from '@/request/index'


const path = '/book/'

export function apiGetHomeBook() {
    return httpRequest({
        url: path + 'getHomeBook/',
        method: 'GET'
    })
}

export function apiGetBookInfo(param) {
    return httpRequest({
        url: path + 'getBookInfo/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetBookChapter(param) {
    return httpRequest({
        url: path + 'getBookChapter/',
        method: 'POST',
        data: getFormData(param)
    })
}


export function apiGetLastReadChapter(param) {
    return httpRequest({
        url: path + 'getLastReadChapter/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiSetBookCollect(param) {
    return httpRequest({
        url: path + 'setBookCollect/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetChapterContent(param) {
    return httpRequest({
        url: path + 'getChapterContent/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiAddBookHistory(param) {
    return httpRequest({
        url: path + 'addBookHistory/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetBookHistory(param) {
    return httpRequest({
        url: path + 'getBookHistory/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetBookCollections(param) {
    return httpRequest({
        url: path + 'getBookCollections/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiDeleteBookCollections(param) {
    return httpRequest({
        url: path + 'deleteBookCollections/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiDeleteBookHistory(param) {
    return httpRequest({
        url: path + 'deleteBookHistory/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetBookSearch(param) {
    return httpRequest({
        url: path + 'getBookSearch/',
        method: 'POST',
        data: getFormData(param)
    })
}
