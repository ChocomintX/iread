<template>
  <van-sticky z-index="45">
    <div id="head-group">
      <div class="head-btn" style="padding-left: 10px">
        <van-icon name="gem-o" size="25"/>
      </div>
      <van-search
          placeholder="搜索作品名"
          readonly
          :style="{height:'100%'}"
          v-on:click="this.$router.push('/search')"
      />
      <div class="head-btn" style="padding-right: 10px">
        <van-icon v-on:click="showMenu=!showMenu" name="apps-o" size="25"/>
      </div>
    </div>
  </van-sticky>

  <!--  <transition name="action-fade">-->
  <div v-if="showMenu" id="head-action-group">
    <div class="head-action-item" v-on:click="this.$router.push('/collection')">
      <van-icon name="bar-chart-o" size="20"></van-icon>
      <div style="margin-top: 5px">书架</div>
    </div>
    <div class="head-action-item" v-on:click="this.$router.push('/history')">
      <van-icon name="underway-o" size="20"></van-icon>
      <div style="margin-top: 5px">历史</div>
    </div>
    <div class="head-action-item" v-on:click="this.$router.push('/user')">
      <van-icon name="user-o" size="20"></van-icon>
      <div style="margin-top: 5px">我的</div>
    </div>
  </div>
  <!--  </transition>-->
  <!--  <div v-show="showMenu" class="overlay-class" v-on:click="showMenu=false"/>-->
  <van-overlay :show="showMenu" @click="showMenu = false" :style="{top:'50px'}"/>
  <van-tabs v-model:active="activePage">
    <van-tab title="漫画">
      <manga-home-page></manga-home-page>
    </van-tab>
    <van-tab title="小说">
      <book-home-page></book-home-page>
      <!--      {{ title }}-->
      <!--      <van-button v-on:click="testApi" type="primary">按钮</van-button>-->
      <!--      <button>按钮</button>-->
      <!--      <router-link to="/login">登录</router-link>-->
      <!--      <router-link to="/register">注册</router-link>-->
      <!--      <img style="width: 100%" v-for="(img,index) in images" :key="index" :src="img">-->

    </van-tab>
  </van-tabs>
</template>

<script>
import {apiGetUserInfo} from "@/apis/test";
import MangaHomePage from "@/page/mangaHomePage";
import BookHomePage from "@/page/bookHomePage";

export default {
  name: "HomePage",
  components: {BookHomePage, MangaHomePage},
  data() {
    return {
      title: "主页",
      searchText: "搜索作品名",
      showMenu: false,
      activePage: 0,
      images: [],
      testApi() {
        // let param = new URLSearchParams();
        // param.append("chapter_url", "http://www.ykmh.com/manhua/kexuecunzaiderenwainiangguanchariji/34754.html");
        // param.append("cookie", localStorage.getItem("cookie"));
        let param = {
          "chapter_url": "http://www.ykmh.com/manhua/kexuecunzaiderenwainiangguanchariji/34754.html"
        }


        apiGetUserInfo(param).then(res => {
          console.log(res)
        })
      },
    }
  },
  methods: {
    init() {
      window.scrollTo(0, 1)
      this.showMenu = false
    }
  },
  created() {
    this.init()
  },
  activated() {
    console.log("加载缓存界面：主页")
  },
  deactivated() {
  }

}
</script>

<style scoped>
@import "../assets/app.css";

.van-search {
  flex-grow: 1;
}

#head-group {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;

  background-color: white;
}

.head-btn {
  width: 10%;
  max-width: 50px;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

@-webkit-keyframes example {
  from {
    top: -30px
  }
  to {
    top: 50px
  }
}

.action-fade-enter-active {
  animation: example 0.5s;
}

.action-fade-leave-active {
  animation: example 0.3s reverse;
}

#head-action-group {
  position: fixed;
  top: 50px;
  z-index: 2;
  height: 70px;
  width: 100%;
  background-color: white;

  display: flex;
  justify-content: center;
  align-items: center;
}

.head-action-item {
  flex-grow: 0.33;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: 15px;
}


.overlay-class {
  position: fixed;
  z-index: -2;
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  height: 100%;
}


</style>