<template>
  <div v-if="!loadingPage" style="overflow-y: hidden">
    <van-share-sheet
        v-model:show="showShare"
        title="立即分享给好友"
        :options="shareOptions"
    />
    <transition name="van-slide-down">
      <div id="view-head" v-if="showMenu">
        <div id="view-head-left">
          <van-icon name="arrow-left" size="18" v-on:click="this.$router.back()"/>
        </div>
        <div id="view-head-content">{{ chapters[chapterIndex].name }}</div>
        <div id="view-head-right">
          <van-icon v-on:click="showShare=true" name="share-o" size="18"/>
        </div>
        <!--      <div style="background-image: linear-gradient(180deg, #ffffff 0%, #000000 100%);height: 1px"></div>-->
      </div>
    </transition>

    <div id="view-content" style="overflow-y: hidden">
      <div v-for="(url,i) in images" :key="i" :style="{filter:'brightness('+settings.brightness+'%)'}">
        <van-image width="100vw" v-on:click="openMenu(i)" @touchmove="imageIndex=i" fit="fill" :src="url"
                   :id="'image_'+i" lazy-load
                   style="display:block;">
          <template v-slot:loading>
            <van-loading type="spinner" size="20"/>
          </template>
        </van-image>
      </div>
    </div>

    <div id="view-foot-info" v-if="!loadingPage" :style="{bottom:showMenu?'135px':0}">
      <div id="view-foot-info-left">
        <div>{{ browserNameVersion }}</div>
        <div>{{ time }}</div>
      </div>
      <div id="view-foot-info-right">
        <div>{{ chapter.name }}</div>
        <div>{{ imageIndex + 1 + "/" + images.length }}</div>
      </div>
    </div>

    <transition name="van-fade">
      <div id="brightness-group" v-if="showBrightness">
        <van-icon name="closed-eye"/>
        <van-slider v-model="settings.brightness" bar-height="5px"/>
        <van-icon name="eye-o"/>
      </div>
    </transition>

    <transition name="van-slide-up">
      <div id="view-foot" v-if="showMenu">
        <div class="slider-group">
          <div v-on:click="openChapter(chapterIndex-1)">上一话</div>
          <van-slider v-model="imageIndex" :max="images.length-1" bar-height="5px" @change="onImageSliderChange()"/>
          <div v-on:click="openChapter(chapterIndex+1)">下一话</div>
        </div>
        <div id="view-foot-button-group">
          <div class="view-foot-button-item" v-for="(btn,index) in footButtons" :key="index"
               v-on:click="btnClick(index)"
               :style="{color:btn.color}">
            <transition name="van-fade">
              <van-icon v-if="!btn.loading" size="25" :color="btn.icon_color" :name="btn.icon"
                        :badge="btn.badge"></van-icon>
            </transition>

            <!--            <van-loading v-if="btn.loading" color="white" size="25"/>-->
            <transition name="van-fade">
              <div style="margin-top: 5px">{{ btn.text }}</div>
            </transition>
          </div>

        </div>
      </div>
    </transition>

    <van-action-sheet v-model:show="showChapterList" :style="{'background-color':'black' ,color:'white',height:'70%'}">
      <div id="chapter-group">
        <div class="van-hairline--bottom">
          <div>全部章节({{ chapters.length }})</div>
          <div :style="{color:chapterListOrder?'#1989fa':'white'}"
               v-on:click="chapterListOrder=!chapterListOrder">
            <div>{{ chapterListOrder ? "倒序" : "正序" }}</div>
            <van-icon name="exchange"/>
          </div>
        </div>
        <div>
          <div v-for="(item,index) in chapters" :key="index" :id="'chapter_'+index"
               class="van-hairline--bottom chapter-item">
            <span>
              {{ item.name }}
              <van-tag v-if="index===chapterIndex" plain type="primary"
                       :style="{'background-color':'rgba(0,0,0,0'}">当前章节</van-tag>
            </span>
            <van-button plain color="white" size="small" :style="{'background-color':'rgba(0,0,0,0)'}" icon="arrow"
                        icon-position="right" v-on:click="openChapter(index)">阅读该话
            </van-button>
          </div>
        </div>
      </div>
    </van-action-sheet>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import {apiAddMangaHistory, apiGetMangaChapterImages, apiSetMangaCollect} from "@/apis/mangaApis";
import {getBrowserNameVersion} from "@/global/utils";
import {Toast} from "vant";

export default {
  name: "mangaViewPage",
  // inject:['reload'],
  data() {
    return {
      loadingPage: true,
      showMenu: false,
      mangaHistory: {},
      chapters: [],
      chapter: {},
      images: [],
      imageIndex: 0,
      chapterIndex: 0,
      footButtons: [],
      settings: {
        brightness: 100,
      },
      showBrightness: false,
      showChapterList: false,
      chapterListOrder: false,
      time: "",
      browserNameVersion: getBrowserNameVersion(),
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
    }
  },
  methods: {
    openMenu(imageIndex) {
      this.showBrightness = false
      this.showMenu = !this.showMenu
      this.imageIndex = imageIndex
      console.log(imageIndex)
    },
    onImageSliderChange() {
      const img = document.querySelector('#image_' + this.imageIndex)
      img.scrollIntoView()
    },
    btnClick(index) {
      this[this.footButtons[index]["clickable"]](index)
    },
    setCollect(index) {
      const isCollect = (this.mangaHistory.collect === 0)
      const mangaInfo = JSON.parse(localStorage.getItem("currentMangaInfo"))
      this.footButtons[index]["loading"] = true
      apiSetMangaCollect({
        user_id: this.$user.id,
        manga_id: mangaInfo.id,
        collect: isCollect ? 1 : 0
      }).then(res => {
        localStorage.setItem("currentMangaHistory", JSON.stringify(res.data))
        this.mangaHistory = res.data
        this.footButtons[index]["text"] = (isCollect ? "已收藏" : "收藏")
        this.footButtons[index]["icon"] = (isCollect ? "star" : "star-o")
        this.footButtons[index]["icon_color"] = (isCollect ? "yellow" : "")
        delete this.footButtons[index]["loading"]

        console.log("setCollect")
      })
    },
    setBrightness(index) {
      this.showMenu = false
      this.showBrightness = true
      console.log("setBrightness", index)
    },
    openCommentList(index) {
      this.$Toast.fail("暂未开通此功能,敬请期待");
      console.log("openCommentList", index)
    },
    openChapterList(index) {
      this.showMenu = false
      this.showChapterList = true

      var id = setInterval(() => {
        const chapter = document.querySelector('#chapter_' + this.chapterIndex)
        if (chapter !== null) {
          chapter.scrollIntoView()
          clearInterval(id)
        }
      }, 500)
      console.log("openChapterList", index)
    },
    openChapter(chapterIndex) {
      if (this.chapterListOrder) {
        this.chapterListOrder = false
        chapterIndex = this.chapters.length - chapterIndex - 1
      }
      console.log(chapterIndex)
      if (chapterIndex < 0) {
        Toast.fail("已经是第一章了")
        return
      } else if (chapterIndex > this.chapters.length - 1) {
        Toast.fail("没有更多章节了")
        return
      }
      console.log(chapterIndex)
      this.$router.replace("/mangaView/" + this.$route.params.listIndex + "/" + chapterIndex)
    },
    getTime() {
      const date = new Date()
      this.time = date.getMonth() + "-" + date.getDay() + " " + date.getHours() + ":" + date.getMinutes()
    },
    async init() {
      this.loadingPage = true
      this.showMenu = false
      this.showChapterList = false
      this.chapterListOrder = false
      this.imageIndex = 0

      this.getTime()
      setInterval(this.getTime, 1000)

      const listIndex = this.$route.params.listIndex
      this.chapters = JSON.parse(localStorage.getItem("currentMangaChapterList"))[listIndex].chapter_list
      this.chapterIndex = parseInt(this.$route.params.chapterIndex)
      this.chapter = this.chapters[this.chapterIndex]

      await apiGetMangaChapterImages({
        chapter_url: this.chapter.url
      }).then(res => {
        this.images = res.data
      })

      // const mangaHistory=localStorage.getItem("currentMangaHistory")
      await apiAddMangaHistory({
        user_id: this.$user.id,
        manga_id: JSON.parse(localStorage.getItem("currentMangaInfo")).id,
        last_read_chapter: this.chapter.name,
        last_read_url: this.chapter.url,
      }).then(res => {
        localStorage.setItem("currentMangaHistory", JSON.stringify(res.data))
        this.mangaHistory = res.data
      })

      const isCollect = this.mangaHistory.collect
      this.footButtons = [{
        text: isCollect ? "已收藏" : "收藏",
        icon: isCollect ? "star" : "star-o",
        icon_color: isCollect ? "yellow" : "",
        active: false,
        clickable: "setCollect"
      }, {
        text: "亮度",
        icon: "eye-o",
        active: false,
        clickable: "setBrightness"
      }, {
        text: "评论",
        icon: "comment-o",
        badge: "99+",
        active: false,
        clickable: "openCommentList"
      }, {
        text: "章节",
        icon: "orders-o",
        active: false,
        clickable: "openChapterList"
      }]
      this.loadingPage = false
      Toast.clear()
    },
  },
  watch: {
    $route() {
      if (this.$route.fullPath.substring(0, 10) !== "/mangaView")
        return
      Toast.loading({
        message: "加载图片中",
        duration: 0
      })
      this.init()
      document.getElementById("image_0").scrollIntoView()
    },
    chapterListOrder() {
      console.log("setOrder")
      this.chapters.reverse()
      this.chapterIndex = this.chapters.length - this.chapterIndex - 1
      const topChapter = document.querySelector('#chapter_0')
      topChapter.scrollIntoView()
    },
    showChapterList() {
      if (!this.showChapterList)
        this.chapterListOrder = false
    }
  },
  created() {
    Toast.loading({
      message: "加载图片中",
      duration: 0
    })
    this.init()
  }
}
</script>

<style scoped>
#view-head {
  position: fixed;
  width: 100%;
  height: 60px;
  z-index: 1000;
  top: 0;

  font-size: 16px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: rgba(0, 0, 0, 1);
}

#view-head > div {
  display: flex;
  align-items: center;
  justify-content: center;
}

#view-head-left {
  width: 50px;
}

#view-head-content {
  max-width: 60%;
}

#view-head-right {
  width: 50px;
}

#view-content {
  width: 100%;
  min-height: 200px;
}


#view-foot {
  position: fixed;
  width: 100%;
  font-size: 14px;
  z-index: 1000;
  bottom: 0;
  color: white;
  background-color: rgba(0, 0, 0, 0.8);
}

.slider-group {
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slider-group > :first-child, .slider-group > :nth-child(3) {
  flex-grow: 0.5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slider-group > :nth-child(2) {
  width: 50%;
}

#view-foot-button-group {
  height: 70px;
  margin: -10px 0 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-foot-button-item {
  height: 100%;
  width: 25%;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#view-foot-info {
  position: fixed;
  width: 100%;
  font-size: 10px;
  z-index: 1000;
  bottom: 0;
  color: white;
  display: flex;
  justify-content: space-between;

  transition: bottom 0.6s ease;
}

#view-foot-info-left, #view-foot-info-right {
  /*background-color: rgba(0,0,0,0);*/
  display: flex;
  padding: 5px;
  border-radius: 5px;
  background-color: rgba(0, 0, 0, 0.5);
}

#view-foot-info-left > *, #view-foot-info-right > * {
  margin: 0 5px 0 5px;
}

#brightness-group {
  position: fixed;
  width: 60%;
  height: 50px;
  margin: auto;
  display: flex;
  align-items: center;
  left: 0;
  right: 0;
  bottom: 70px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 5px;
  z-index: 1000;
  color: white;
  justify-content: center;
}

#brightness-group > i {
  margin: 0 10px 0 10px;
}

#chapter-group {
  width: 100%;
  height: 100%;
  background-color: black;
  color: white;
  display: flex;
  flex-direction: column;
  overflow: scroll;
}

#chapter-group > :first-child {
  display: flex;
  justify-content: space-between;
  padding: 20px 3% 20px 3%;
}

#chapter-group > :first-child > :nth-child(2) {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  /*padding: 0 3% 0 3%;*/
}

#chapter-group > :nth-child(2) {
  flex-grow: 1;
  overflow: scroll;
  overflow-x: hidden;
  scroll-behavior: smooth;
  padding: 0 3% 0 5%;
}

#chapter-group > :nth-child(2) > div {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
}
</style>