<template>
  <van-empty v-if="isEmpty" description="什么也没有搜到（；´д｀）ゞ"/>
  <div v-show="!loadingPage&&!isEmpty" style="overflow-x: hidden">
    <div v-for="(manga,index) in mangaList" :key="index">
      <div class="history-item van-hairline--bottom" v-on:click="openManga(index)">
        <div>
          <img class="history-img" :src="manga.image_url"/>
        </div>
        <div class="history-info">
          <div class="van-ellipsis"><b v-html="manga.title"></b></div>
          <div v-html="manga.author"></div>
          <div></div>
          <div>最后更新章节</div>
          <div v-html="manga.last_chapter"></div>
        </div>
      </div>
    </div>

  </div>

</template>

<script>
import {Toast} from "vant";
import {apiGetMangaInfo, apiGetMangaSearch} from "@/apis/mangaApis";

export default {
  name: "mangaSearchPage",
  props: ["keywords", "searchCount"],
  data() {
    return {
      loadingPage: true,
      page: 1,
      mangaList: []
    }
  },
  methods: {
    async init() {
      Toast.loading({
        message: "搜索中...",
        duration: 0
      })
      this.loadingPage = true

      await apiGetMangaSearch({
        keywords: this.keywords,
        page: this.page
      }).then(res => {
        let data = JSON.stringify(res.data).replaceAll(this.keywords, "<span style='color:lightskyblue'>" + this.keywords + "</span>")
        this.mangaList = JSON.parse(data)
      })
      //模拟请求成功
      this.loadingPage = false
      Toast.clear()
    },
    async openManga(index){
      Toast.loading({
        message:"爬取漫画信息中...",
        duration:0
      })
      const manga=this.mangaList[index]
      await apiGetMangaInfo({
        manga_url:manga.manga_url
      }).then(res=>{
        Toast.clear()
        localStorage.setItem("currentMangaInfo",JSON.stringify(res.data))
        this.$router.push('/mangaInfo/'+res.data.id)
      })
    }
  },
  computed: {
    isEmpty() {
      return !this.mangaList || this.mangaList.length === 0
    }
  },
  watch: {
    searchCount() {
      console.log(1)
      this.init()
    }
  },
  created() {
    this.init()
  }
}
</script>

<style scoped>
.history-item {
  width: 100%;
  padding: 10px 10px 0 10px;
  display: flex;
}

.history-info {
  margin-left: 10px;
  max-width: calc(100vw - 110px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.history-info > div {
  height: 25px;
  max-width: 100%;
}

.history-img {
  width: 90px;
  height: 120px;
  border-radius: 5px;
}

.delete-button {
  height: 100%;
}
</style>