<template>
  <van-sticky>
    <van-nav-bar title="我的书架" left-text="返回" left-arrow style="height: 50px">
      <template #left>
        <van-icon name="arrow-left" size="18" color="black" v-on:click="this.$router.back()"/>
      </template>
      <template #right>
        <van-icon v-on:click="isEdit=!isEdit" name="filter-o" size="20" :color="isEdit?'#1989fa':'black'"></van-icon>
      </template>
    </van-nav-bar>
  </van-sticky>

  <!-- closeable 模式，在右侧显示关闭按钮 -->
  <!--    <van-notice-bar mode="closeable">点击右上角可以编辑书架哦！</van-notice-bar>-->
  <van-notice-bar color="#1989fa" background="#ecf9ff" :style="{fontSize:'14px',marginBottom:'10px'}" mode="closeable">
    <template #left-icon>
      <van-icon name="info-o" size="16" style="margin-right: 10px"></van-icon>
    </template>
    点击右上角可以编辑书架哦！
  </van-notice-bar>

  <van-tabs v-model:active="active" type="card" color="#999999" @click-tab="isEdit=false">
    <van-tab title="漫画">
      <manga-collection-page :isEdit="isEdit" @setEdit="setEdit"></manga-collection-page>
    </van-tab>
    <van-tab title="小说">
      <book-collection-page :isEdit="isEdit" @setEdit="setEdit"></book-collection-page>
    </van-tab>
  </van-tabs>


</template>

<script>

import MangaCollectionPage from "@/page/mangaCollectionPage";
import BookCollectionPage from "@/page/bookCollectionPage";
export default {
  name: "collectionPage",
  components: {BookCollectionPage, MangaCollectionPage},
  data() {
    return {
      isEdit: false,
      active:0
    }
  },
  methods:{
    setEdit(value){
      this.isEdit=value
    }
  }
}
</script>

<style scoped>


</style>