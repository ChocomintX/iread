<template>
  <van-sticky>
    <van-nav-bar title="历史记录" left-text="返回" left-arrow style="height: 50px">
      <template #left>
        <van-icon name="arrow-left" size="18" color="black" v-on:click="this.$router.back()"/>
      </template>
    </van-nav-bar>
  </van-sticky>
  <van-notice-bar color="#1989fa" background="#ecf9ff" :style="{marginBottom:'10px'}" mode="closeable">
    <template #left-icon>
      <van-icon name="info-o" size="16" style="margin-right: 10px"></van-icon>
    </template>
    左划可以收藏，右滑可以删除记录哦！(｡･∀･)ﾉﾞ
  </van-notice-bar>
  <van-tabs v-model:active="active" type="card" color="#999999" @click-tab="isEdit=false">
    <van-tab title="漫画">
      <manga-history-page></manga-history-page>
    </van-tab>
    <van-tab title="小说">
      <book-history-page></book-history-page>
    </van-tab>
  </van-tabs>

</template>

<script>
import MangaHistoryPage from "@/page/mangaHistoryPage";
import BookHistoryPage from "@/page/bookHistoryPage";
export default {
  name: "historyPage",
  // eslint-disable-next-line vue/no-unused-components
  components: {BookHistoryPage, MangaHistoryPage},
  data(){
    return{
      activePage: 0,
    }
  }
}
</script>

<style scoped>

</style>