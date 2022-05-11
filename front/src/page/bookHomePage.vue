<template>
  <div style="width: 100%">
    <van-swipe :autoplay="3000" lazy-render>
      <van-swipe-item v-for="image in swipeImages" :key="image">
        <van-image :src="image"></van-image>
      </van-swipe-item>
    </van-swipe>
    <div class="list-group" v-for="(list,i) in homeBooks" :key="i">
      <div class="list-title"><h3>{{ list.title }}</h3></div>
      <div class="list-top" v-on:click="openBook(list.top_book.book_url)">
        <van-image class="list-top-img" :src="list.top_book.image_url"/>
        <div class="list-top-info">
          <div><b>{{ list.top_book.name }}</b></div>
          <div class="list-top-detail" style="margin-top: 5px">{{ list.top_book.detail }}</div>
        </div>
      </div>
      <div class="list-item-group">
        <div class="list-item van-ellipsis" v-for="(book,j) in list.book_list" :key="j" v-on:click="openBook(book.book_url)">
          <span style="color: lightskyblue">
            {{ book.name }}
          </span>
          /
          <span style="color: #999999;font-size: 10px">
            {{ book.author }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {apiGetBookInfo, apiGetHomeBook} from "@/apis/bookApis";

export default {
  name: "bookHomePage",
  data() {
    return {
      homeBooks: [],
      loadingPage: true,
      swipeImages: ["https://f2.kkmh.com/image/220412/GAIafzm3C.png-t.w1125.png.h", "https://f2.kkmh.com/image/220412/GAIafzm3C.png-t.w1125.png.h", "https://f2.kkmh.com/image/220412/GAIafzm3C.png-t.w1125.png.h"],
    }
  },
  methods: {
    async init() {
      await apiGetHomeBook().then(res => this.homeBooks = res.data)
    },
    openBook(url){
      console.log(url)
      apiGetBookInfo({
        book_url:url
      }).then(res=>{
        localStorage.setItem("currentBookInfo",res.data)
        this.$router.push("/bookInfo/"+res.data.id)
      })
    }
  },
  created() {
    this.init()
  }
}
</script>

<style scoped>
.list-group {
  width: calc(100% - 10px);
  padding: 0 5px 0 5px;
}

.list-title {
  background-color: #999999;
  margin: 5px 0 10px 0px
}

.list-top {
  display: flex;
}

.list-top-img {
  width: 120px;
  height: 160px;
}

.list-top-info {
  width: 60%;
  padding-left: 5%;
}

.list-top-detail {
  display: -webkit-box;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 6;
  -webkit-box-orient: vertical;
}

.list-item-group {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
}

.list-item {
  width: 50%;
  height: 30px;
}
</style>