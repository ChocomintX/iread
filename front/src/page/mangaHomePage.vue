<template>
  <div v-if="loadingPage">
    <van-swipe :autoplay="3000" lazy-render>
      <van-swipe-item v-for="image in swipeImages" :key="image">
        <van-image :src="image"></van-image>
      </van-swipe-item>
    </van-swipe>

<!--    <div class="btn-box">-->
<!--      <van-button plain round size="large" icon="apps-o" style="margin-right: 5px" color="black">作品分类</van-button>-->
<!--      &lt;!&ndash;      color="linear-gradient(147deg, #FF2525 0%, #e9ef36 90%)"&ndash;&gt;-->
<!--      <van-button plain round size="large" icon="bar-chart-o" color="black">作品排行</van-button>-->
<!--      &lt;!&ndash;      color="linear-gradient(147deg, #0093E9 0%, #80D0C7 74%)"&ndash;&gt;-->
<!--    </div>-->

    <div class="manga-group" v-for="(list,index) in mangaLists" :key="index">
      <h3 class="list-title">{{ list.title }}</h3>
      <div class="grid">
        <div class="grid-item" v-on:click="mangaInfo(item)" v-for="(item,i) in list.data.slice(0,6)" :key="i">
          <van-image radius="10" width="100%" height="42vw" fit="cover" :src="item.image_url"></van-image>
          <div class="manga-title">{{ item.title }}</div>
          <div class="manga-tag">{{ item.category.name }}</div>
        </div>
      </div>
      <div class="btn-box">
        <van-button plain style="margin-right: 5px" color="#666666">查看更多</van-button>
        <van-button color="#666666" v-on:click="change(index)">换一换</van-button>
      </div>
    </div>
  </div>
</template>

<script>

import {apiGetHomeManga} from "@/apis/mangaApis";
import {Toast} from "vant";

export default {
  name: "mangaHomePage",
  data() {
    return {
      loadingPage:true,
      swipeImages: ["https://f2.kkmh.com/image/220412/TVBN86Qc5.png-t.w1125.png.h","https://f2.kkmh.com/image/220412/TVBN86Qc5.png-t.w1125.png.h"],
      mangaLists: []
    }
  },
  methods: {
    mangaInfo(item) {
      localStorage.setItem("currentMangaInfo", JSON.stringify(item))
      this.$router.push("/mangaInfo/" + item.id)
    },
    change(index){
      this.mangaLists[index].data.sort(()=>{
        return Math.random()-0.5
      })
    },
    async init(){
      await apiGetHomeManga().then(res=>this.mangaLists=res.data)
      Toast.clear()
    }
  },
  created() {
    Toast.loading({
      message:"加载中",
      duration:0
    })
    this.init()
  },
  activated() {
    console.log("缓存界面")
  }
}
</script>

<style scoped>
@import "../assets/app.css";

.manga-group {
  padding-bottom: 10px;
}

.grid {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.grid-item {
  width: 31%;
  margin: 0 1% 5px 1%;
}

.list-title {
  margin: 5px 0 10px 5px;
}

.manga-title {
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.manga-tag {
  /*background-color: linear-gradient(147deg, #FF2525 0%, #e9ef36 74%);*/
  font-size: 10px;
  color: #999;
}

.btn-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-top: 20px;
  margin-bottom: 20px;
}

.btn-box > * {
  width: 48%;
  /*margin: 0 2% 0 2%;*/
}
</style>