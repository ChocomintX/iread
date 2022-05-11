import httpRequest from '@/request/index'
import {getFormData} from "@/utils/formDataUtil"

const path = '/manga/'

export function apiGetHotManga() {
    return httpRequest({
        url: path + 'getHotManga/',
        method: 'POST'
    })
}

export function apiGetHomeManga() {
    return httpRequest({
        url: path + 'getHomeManga/',
        method: 'POST'
    })
}

export function apiGetMangaInfo(param) {
    return httpRequest({
        url: path + 'getMangaInfo/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetMangaChapterList(param) {
    return httpRequest({
        url: path + 'getMangaChapterList/',
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

export function apiAddMangaHistory(param) {
    return httpRequest({
        url: path + 'addMangaHistory/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiSetMangaCollect(param) {
    return httpRequest({
        url: path + 'setMangaCollect/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetMangaChapterImages(param) {
    return httpRequest({
        url: path + 'getMangaChapterImages/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetMangaHistory(param) {
    return httpRequest({
        url: path + 'getMangaHistory/',
        method: 'POST',
        data: getFormData(param)
    })
}


export function apiDeleteMangaHistory(param) {
    return httpRequest({
        url: path + 'deleteMangaHistory/',
        method: 'POST',
        data: getFormData(param)
    })
}


export function apiGetMangaCollections(param) {
    return httpRequest({
        url: path + 'getMangaCollections/',
        method: 'POST',
        data: getFormData(param)
    })
}


export function apiDeleteMangaCollections(param) {
    return httpRequest({
        url: path + 'deleteMangaCollections/',
        method: 'POST',
        data: getFormData(param)
    })
}

export function apiGetMangaSearch(param) {
    return httpRequest({
        url: path + 'getMangaSearch/',
        method: 'POST',
        data: getFormData(param)
    })
}