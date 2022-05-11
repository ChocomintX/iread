<template>
  <div v-show="!isEmpty&&!loadingPage" style="margin-top: 10px">
    <div v-for="(history,index) in historyList" :key="index">
      <van-swipe-cell>
        <template #left>
          <van-button square type="primary" v-on:click="setCollect(index)" :text="history.collect?'取消收藏':'收藏漫画'"
                      class="delete-button"/>
        </template>
        <div class="history-item van-hairline--bottom" v-on:click="this.$router.push('/mangaInfo/'+history.manga.id)">
          <div>
            <img class="history-img" :src="history.manga.image_url"/>
          </div>
          <div class="history-info">
            <div class="van-ellipsis"><b>{{ history.manga.title }}</b></div>
            <div>{{ history.manga.author.name }}</div>
            <!--            <div>{{ history.last_read_chapter }}</div>-->
            <div></div>
            <div>上次阅读时间</div>
            <div>{{ stampToTime(history.last_read_time) }}</div>
          </div>
        </div>
        <template #right>
          <van-button square v-on:click="deleteHistory(index)" text="删除" type="danger" class="delete-button"/>
        </template>
      </van-swipe-cell>
    </div>
  </div>
  <van-empty v-if="isEmpty" description="这里什么都没有(っ °Д °;)っ"/>
</template>

<script>
import {Toast} from "vant";
// eslint-disable-next-line no-unused-vars
import {apiDeleteMangaHistory, apiGetMangaHistory, apiSetMangaCollect} from "@/apis/mangaApis";

export default {
  name: "mangaHistoryPage",
  data() {
    return {
      loadingPage: true,
      historyList: []
    }
  },
  methods: {
    async init() {
      Toast.loading({
        message: "获取浏览历史中...",
        duration: 0
      })
      this.loadingPage = true

      await apiGetMangaHistory({
        user_id: this.$user.id
      }).then(res => this.historyList = res.data)
      //模拟请求成功
      this.loadingPage = false
      Toast.clear()
    },
    stampToTime(stamp) {
      stamp = parseInt(stamp * 1000)
      const date = new Date(stamp)
      const res = date.getFullYear() + "-"
          + (date.getMonth() + 1) + "-"
          + date.getDate() + " "
          + date.getHours() + ":"
          + (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes())
      return res
    },
    async setCollect(index) {
      Toast.loading({
        message: "请求中",
        duration: 0
      })
      const collect = this.historyList[index].collect
      const manga_id = this.historyList[index].manga.id
      await apiSetMangaCollect({
        user_id: this.$user.id,
        manga_id: manga_id,
        collect: collect === 0 ? 1 : 0
      })

      await apiGetMangaHistory({
        user_id: this.$user.id
      }).then(res => {
        this.historyList = res.data
      })
      Toast.clear()
    },
    async deleteHistory(index) {
      Toast.loading({
        message: "请求中",
        duration: 0
      })

      const user_id = this.$user.id
      const manga_id = this.historyList[index].manga.id

      await apiDeleteMangaHistory({
        user_id: user_id,
        manga_id: manga_id,
      }).then((res) => {
        this.historyList = res.data
      })

      // delete this.historyList[index]
      Toast.clear()
    }

  },
  computed: {
    isEmpty() {
      return this.historyList.length === 0
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