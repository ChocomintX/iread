<template>
  <div v-if="!loadingPage" style="width: 100%">
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
      </div>
    </transition>

    <div id="view-content"
         :style="styleObject"
         v-on:click="openMenu()" v-html="content">
    </div>

    <div id="view-foot-info" v-if="!loadingPage" :style="{bottom:showMenu?'135px':0}">
      <div id="view-foot-info-left" class="van-ellipsis">
        <div>{{ browserNameVersion }}</div>
        <div>{{ time }}</div>
      </div>
      <div id="view-foot-info-right">
        <div class="van-ellipsis">{{ chapter.name }}</div>
      </div>
    </div>

    <transition name="van-fade">
      <div>
        <div id="brightness-group" v-if="showBrightness">
          <van-icon name="closed-eye"/>
          <van-slider v-model="settings.brightness" bar-height="5px"/>
          <van-icon name="eye-o"/>
        </div>
        <div id="settings-group" v-if="showSettings">
          <div>
            <span>字体大小</span>
            <van-stepper v-model="settings.fontSize"/>
          </div>
          <div>
            <span>字体颜色</span>
            <div style="display: flex;justify-content: space-between;width: 50%">
              <div v-on:click="settings.fontColor='black'" style="width: 20px;height:20px;background-color: black"></div>
              <div v-on:click="settings.fontColor='white'" style="width: 20px;height:20px;background-color: white"></div>
              <div v-on:click="settings.fontColor='red'" style="width: 20px;height:20px;background-color: red"></div>
            </div>
          </div>
          <div>
            <span>背景颜色</span>
            <div style="display: flex;justify-content: space-between;width: 50%">
              <div v-on:click="settings.backgroundColor='black'" style="width: 20px;height:20px;background-color: black"></div>
              <div v-on:click="settings.backgroundColor='white'" style="width: 20px;height:20px;background-color: white"></div>
              <div v-on:click="settings.backgroundColor='rgb(212, 209, 209)'" style="width: 20px;height:20px;background-color: rgb(212, 209, 209)"></div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <transition name="van-slide-up">
      <div id="view-foot" v-if="showMenu">
        <div class="slider-group">
          <div v-on:click="openChapter(chapterIndex-1)">上一话</div>
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

import {getBrowserNameVersion} from "@/global/utils";
import {Toast} from "vant";
import {apiAddBookHistory, apiGetChapterContent, apiSetBookCollect} from "@/apis/bookApis";

export default {
  name: "bookViewPage",
  data() {
    return {
      loadingPage: true,
      showMenu: false,
      showSettings: false,
      bookHistory: {},
      chapters: [],
      chapter: {},
      content: "",
      images: [],
      imageIndex: 0,

      chapterIndex: 0,
      footButtons: [],
      settings: {
        brightness: 100,
        backgroundColor: "#d4d1d1",
        fontColor: "#000000",
        fontSize: "15"
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
    openMenu() {
      this.showBrightness = false
      this.showSettings = false
      this.showMenu = !this.showMenu
    },
    btnClick(index) {
      this[this.footButtons[index]["clickable"]](index)
    },
    setCollect(index) {
      const isCollect = (this.bookHistory.collect === 0)
      const bookInfo = JSON.parse(localStorage.getItem("currentBookInfo"))
      this.footButtons[index]["loading"] = true
      apiSetBookCollect({
        user_id: this.$user.id,
        book_id: bookInfo.id,
        collect: isCollect ? 1 : 0
      }).then(res => {
        localStorage.setItem("currentBookHistory", JSON.stringify(res.data))
        this.bookHistory = res.data
        this.footButtons[index]["text"] = (isCollect ? "已收藏" : "收藏")
        this.footButtons[index]["icon"] = (isCollect ? "star" : "star-o")
        this.footButtons[index]["icon_color"] = (isCollect ? "yellow" : "")
        delete this.footButtons[index]["loading"]

        console.log("setCollect")
      })
    },
    setBrightness(index) {
      this.showMenu = false
      this.showSettings = false
      this.showBrightness = true
      console.log("setBrightness", index)
    },
    openSettingsMenu(index) {
      this.showMenu = false
      this.showSettings = true
      this.showBrightness = false
      // this.$Toast.fail("暂未开通此功能,敬请期待");
      console.log("openSettingsMenu", index)
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
      this.$router.replace("/bookView/" + chapterIndex)
    },
    getTime() {
      const date = new Date()
      this.time = date.getMonth() + "-" + date.getDay() + " " + date.getHours() + ":" +
          (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes())
    },
    setThemeColor(newColor) {
      this.settings.backgroundColor = newColor
      let metas = document.getElementsByTagName("meta")
      for (let i = 0; i < metas.length; i++) {
        if (metas[i].name === "theme-color") {
          metas[i].remove()
          break;
        }
      }
      const meta = document.createElement('meta');
      meta.content = newColor;
      meta.name = "theme-color";
      document.getElementsByTagName('head')[0].appendChild(meta)
    },
    async init() {
      Toast.loading({
        message: "加载图片中",
        duration: 0
      })
      this.loadingPage = true
      this.showMenu = false
      this.showChapterList = false
      this.showSettings = false
      this.chapterListOrder = false
      this.imageIndex = 0

      this.getTime()
      setInterval(this.getTime, 1000)

      this.chapters = JSON.parse(localStorage.getItem("currentBookChapterList"))
      this.chapterIndex = parseInt(this.$route.params.chapterIndex)
      this.chapter = this.chapters[this.chapterIndex]

      await apiGetChapterContent({
        chapter_url: this.chapter.url
      }).then(res => {
        this.content = res.data
      })

      await apiAddBookHistory({
        user_id: this.$user.id,
        book_id: JSON.parse(localStorage.getItem("currentBookInfo")).id,
        last_read_chapter: this.chapter.name,
        last_read_url: this.chapter.url,
      }).then(res => {
        localStorage.setItem("currentBookHistory", JSON.stringify(res.data))
        this.bookHistory = res.data
      })

      const isCollect = this.bookHistory.collect
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
        text: "设置",
        icon: "setting-o",
        active: false,
        clickable: "openSettingsMenu"
      }, {
        text: "章节",
        icon: "orders-o",
        active: false,
        clickable: "openChapterList"
      }]
      this.loadingPage = false
      Toast.clear()
      this.setThemeColor(this.settings.backgroundColor)
    },
  },
  computed: {
    styleObject() {
      const settings = this.settings
      return {
        filter: 'brightness(' + settings.brightness + '%)',
        backgroundColor: settings.backgroundColor,
        fontSize: settings.fontSize + "px",
        color: settings.fontColor
      }
    }
  },
  watch: {
    $route() {
      console.log(this.$route.fullPath.substring(0, 10))
      if (this.$route.fullPath.substring(0, 10) !== "/bookView/")
        return

      this.init()
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
    },
    settings(){
      console.log(this.settings)
    }
  },
  created() {

    this.init()
  },
  beforeUnmount() {
    this.setThemeColor("white")
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
  width: 96%;
  padding: 0 2% 0 2%;
}

#view-content > div {

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

.slider-group > :first-child, .slider-group > :nth-child(2) {
  width: 50%;
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
  max-width: 40%;
  padding: 5px;
  border-radius: 5px;
  background-color: rgba(0, 0, 0, 0.5);
}

#view-foot-info-left > *, #view-foot-info-right > * {
  margin: 0 5px 0 5px;
}

#view-foot-info-right > * {
  max-width: 100%;
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

#settings-group {
  position: fixed;
  width: 60%;
  height: 150px;
  margin: auto;
  display: flex;
  flex-direction: column;
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

#settings-group > div {
  width: 80%;
  height: 30%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#settings-group > div > i {
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