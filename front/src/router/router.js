import {createRouter, createWebHashHistory} from "vue-router";
import homePage from "@/page/homePage";
import loginPage from "@/page/loginPage";
import registerPage from "@/page/registerPage";
import searchPage from "@/page/searchPage";
import mangaHomePage from "@/page/mangaHomePage";
import mangaInfoPage from "@/page/mangaInfoPage";
import mangaViewPage from "@/page/mangaViewPage";
import collectionPage from "@/page/collectionPage";
import historyPage from "@/page/historyPage";
import mangaHistoryPage from "@/page/mangaHistoryPage";
import bookHistoryPage from "@/page/bookHistoryPage";
import userPage from "@/page/userPage";
import bookInfoPage from "@/page/bookInfoPage";
import bookViewPage from "@/page/bookViewPage";

/**
 * 创建路由对象
 */
const routes = [{
    path: '/',
    redirect: '/login'
},
    {path: '/home', component: homePage, meta: {keepAlive: true}},
    {path: '/user', component: userPage},
    {path: '/login', component: loginPage},
    {path: '/register', component: registerPage},
    {path: '/search', component: searchPage},
    {path: '/mangaHome', name: "mangaIHomePage", component: mangaHomePage},
    {path: '/mangaInfo/:id', name: "mangaInfoPage", component: mangaInfoPage, meta: {keepAlive: true}},
    {path: '/mangaView/:listIndex/:chapterIndex', component: mangaViewPage},
    {path: '/collection', component: collectionPage},
    {path: '/history', component: historyPage},
    {path: '/mangaHistory', component: mangaHistoryPage},
    {path: '/bookHistory', component: bookHistoryPage},
    {path: '/bookInfo/:id', name: "bookInfoPage", component: bookInfoPage, meta: {keepAlive: true}},
    {path: '/bookView/:chapterIndex', component: bookViewPage},
]

/**
 * 初始化路由 配置
 */
const router = createRouter({
    history: createWebHashHistory(),
    routes
});

/**
 * 导出路由
 */
export default router