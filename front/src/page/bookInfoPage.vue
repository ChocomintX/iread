<template>
  <div style="overflow-x: hidden" v-if="!loadingPage">
    <van-share-sheet
        v-model:show="showShare"
        title="立即分享给好友"
        :options="shareOptions"
    />
    <van-nav-bar :title="bookInfo.name" left-text="返回" left-arrow>
      <template #left>
        <van-icon name="arrow-left" size="18" color="black" v-on:click="this.$router.back()"/>
      </template>
      <template #right>
        <van-icon v-on:click="showShare=true" name="share-o" size="18" color="black"/>
      </template>
    </van-nav-bar>
    <div id="info-group">
      <div id="info-img-group">
        <van-image radius="5" height="150" width="112.5" fit="fill" :src="bookInfo.image_url"></van-image>
      </div>
      <div id="info-text-group">
        <div>
          <van-icon name="user-o"/>
          <span>{{ bookInfo.author.name }}</span>
        </div>
        <div>
          <van-icon name="description"/>
          <span>{{ stampToTime(bookInfo.update_time) }}</span>
        </div>
        <div>
          <van-icon name="description"/>
          <span>{{ bookInfo.new_chapter_name }}</span>
        </div>
        <div>
          <van-icon name="edit"/>
          <span>{{ bookInfo.status }}</span>
        </div>
        <div>
          <van-icon name="clock-o"/>
          <span v-if="bookHistory.is_read===0">还没有阅读过该小说</span>
          <span v-if="bookHistory.is_read===1">上次读到:{{ bookHistory.last_read_chapter }}</span>
        </div>

        <div id="info-button-group">
          <div id="read-button" v-on:click="startRead">
            <span>开始阅读</span>
          </div>
          <div id="collect-button" v-on:click="setCollect">
            <span>{{ collectStatus }}</span>
          </div>
        </div>
      </div>
    </div>
    <div id="detail-group" v-on:click="hiddenDetail=!hiddenDetail" :class="hiddenDetail?'detail-hidden':''">
      简介:{{ bookInfo.detail }}
    </div>
    <div class="chapter-group">
      <div class="chapter-list-title-group">
        <div>
          <van-icon name="bookmark-o"/>
          <b>章节目录</b>
        </div>
        <div v-on:click="orderList()" :class="orderType===0?'chapter-order':''">
          排序方式:{{ orderType === 0 ? "倒序" : "正序" }}
          <van-icon name="exchange"/>
        </div>
      </div>
      <div class="chapter-list">
        <div class="chapter-item" v-for="(chapter,index) in bookChapterList" :key="index"
             v-on:click="openChapter(index)">
          <div v-if="!isNewChapter(index)">
            <div class="van-ellipsis">{{ chapter.name }}</div>
          </div>
          <van-badge v-if="isNewChapter(index)" :offset="[-5,3]">
            <div>
              <div class="van-ellipsis">{{ chapter.name }}</div>
            </div>
            <template #content>
              <div>新!</div>
            </template>
          </van-badge>
        </div>

        <div class="blank-item" v-for="j in blankNum()" :key="j"></div>
      </div>
    </div>
  </div>
</template>

<script>
import {Dialog, Toast} from "vant";
import {apiGetBookChapter, apiGetBookInfo, apiGetLastReadChapter, apiSetBookCollect} from "@/apis/bookApis";

export default {
  name: "bookInfoPage",
  data() {
    return {
      loadingPage: true,
      bookInfo: {},
      bookChapterList: [],
      bookHistory: {},
      showShare: false,
      shareOptions: [
        {name: '微信', icon: 'wechat'},
        {name: '朋友圈', icon: 'wechat-moments'},
        {name: '微博', icon: 'weibo'},
        {name: 'QQ', icon: 'qq'},
        {name: '复制链接', icon: 'link'},
        {name: '分享海报', icon: 'poster'},
        {name: '二维码', icon: 'qrcode'},
        {name: '小程序码', icon: 'weapp-qrcode'},
      ],
      hiddenDetail: true,
      orderType: 1
    }
  },
  methods: {
    async init() {
      Toast.loading({
        message: "加载信息中",
        duration: 0
      })

      this.loadingPage = true

      const book_id = this.$route.params.id
      await apiGetBookInfo({
        book_id: book_id,
      }).then(res => {
        localStorage.setItem("currentBookInfo", JSON.stringify(res.data))
        this.bookInfo = res.data
      })

      await apiGetBookChapter({
        book_url: this.bookInfo.book_url
      }).then(res => {
        localStorage.setItem("currentBookChapterList", JSON.stringify(res.data))
        this.bookChapterList = res.data
      })

      const user_id = this.$user.id
      await apiGetLastReadChapter({
        user_id: user_id,
        book_id: this.bookInfo.id
      }).then(res => {
        this.bookHistory = res.data
      })

      this.loadingPage = false
      Toast.clear()
    },
    blankNum() {
      return 4 - this.bookChapterList.length % 4
    },
    isNewChapter(index, chapterIndex) {
      const chapter_list = this.bookChapterList
      const orderType = this.orderType
      const newChapterIndex = (orderType === 0 ? 0 : chapter_list.length - 1)
      return chapterIndex === newChapterIndex
    },
    orderList() {
      this.orderType = this.orderType === 0 ? 1 : 0
      this.bookChapterList.reverse()
    },
    openChapter(chapterIndex) {
      if (this.orderType === 0)
        this.$router.push("/bookView/" + (this.bookChapterList.length - chapterIndex - 1))
      else
        this.$router.push("/bookView/" + chapterIndex)
    },
    startRead() {
      if (this.bookHistory) {
        Dialog.confirm({
          title: "提示",
          message: "上次看到" + this.bookHistory.last_read_chapter + ",是否继续阅读？"
        }).then(() => {

        }).catch(() => {
          // on cancel
        });
      }
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
    async setCollect() {
      const collect = this.bookHistory.collect
      Dialog.confirm({
        title: '提示',
        message: collect === 0 ? "确认将该小说加入书架吗？" : "确认将该小说从书架中移除吗？",
      }).then(() => {
        apiSetBookCollect({
          user_id: this.$user.id,
          book_id: this.bookInfo.id,
          collect: collect === 0 ? 1 : 0
        }).then(res => {
          localStorage.setItem("currentBookHistory", JSON.stringify(res.data))
          this.bookHistory = res.data
        })
      });
    }
  },
  computed: {
    collectStatus() {
      return this.bookHistory.collect === 0 ? "加入书架" : "移出书架"
    }
  },
  created() {
    this.init()
  },
  activated() {
    console.log(parseInt(this.$route.params.id) , this.bookInfo.id)
    if (parseInt(this.$route.params.id) !== this.bookInfo.id) {
      this.init()
    } else {
      window.scrollTo(0,0)
      console.log("缓存页面:漫画信息页")
    }
  }
}
</script>

<style scoped>

#info-group {
  width: 100%;
  height: 200px;
  /*background-image: linear-gradient(160deg, rgba(0, 147, 233, 0.8) 0%, rgba(128, 208, 199, 0.8) 100%);*/
  background-image: linear-gradient(160deg, #8c08a8 0%, #70daff 100%);

  display: flex;
  align-items: center;
}

#info-img-group {
  margin-left: 3%;
}

#info-img-group > * {
  border: white 1px solid;
}


#info-text-group {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  height: 160px;
}

#info-text-group > div {
  flex-grow: 0.2;
  display: flex;
  align-items: center;
  font-size: 12px;
  color: white;
}

#info-text-group > div > span {
  margin-left: 10px;
}

#info-button-group {
  flex-grow: 1;
}

#read-button, #collect-button {
  max-width: 110px;
  width: 50%;
  height: 35px;
  border: white solid 1px;
  border-radius: 5px;
  font-size: 10px;
  margin-right: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#collect-button > span, #read-button > span {
  max-width: 90%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

#detail-group {
  display: -webkit-box;
  padding: 5px 3% 0 3%;
  font-size: 10px;
}

.detail-hidden {
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chapter-list {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.chapter-list-title-group {
  height: 40px;
  background-color: rgb(245, 245, 245);
  padding: 0 3% 0 3%;
  margin: 5px 0 5px 0;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/*.chapter-list-title-group > * {*/
/*  margin: 0 0 0 0;*/
/*}*/

.chapter-order {
  color: #4592ef;
}

.chapter-item {
  width: 22%;
  height: 40px;
  margin: 5px 1% 0 1%;
  border: 1px solid #dcdcde;
  border-radius: 5px;
}

.chapter-item > div {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chapter-item > div > * {
  max-width: 70%;
}

.blank-item {
  width: 22%;
  height: 40px;
  border: 1px solid rgba(0, 0, 0, 0);
  margin: 5px 1% 0 1%;
}

.chapter-item > * {
  font-size: 10px;
}
</style>