<template>
  <div v-show="!isEmpty&&!loadingPage" style="margin-top: 10px">
    <div v-for="(history,index) in historyList" :key="index">
      <van-swipe-cell>
        <template #left>
          <van-button square type="primary" v-on:click="setCollect(index)" :text="history.collect?'取消收藏':'收藏漫画'"
                      class="delete-button"/>
        </template>
        <div class="history-item van-hairline--bottom" v-on:click="this.$router.push('/bookInfo/'+history.book.id)">
          <div>
            <img class="history-img" :src="history.book.image_url"/>
          </div>
          <div class="history-info">
            <div class="van-ellipsis"><b>{{ history.book.name }}</b></div>
            <div>{{ history.book.author.name }}</div>
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
import {apiDeleteBookHistory, apiGetBookHistory, apiSetBookCollect} from "@/apis/bookApis";

export default {
  name: "bookHistoryPage",
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

      await apiGetBookHistory({
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
      const book_id = this.historyList[index].book.id
      await apiSetBookCollect({
        user_id: this.$user.id,
        book_id: book_id,
        collect: collect === 0 ? 1 : 0
      })

      await apiGetBookHistory({
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
      const book_id = this.historyList[index].book.id

      await apiDeleteBookHistory({
        user_id: user_id,
        book_id: book_id,
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