<template>
  <div>
    <van-nav-bar title="个人主页" left-text="返回" left-arrow style="height: 50px">
      <template #left>
        <van-icon name="arrow-left" size="18" color="black" v-on:click="this.$router.back()"/>
      </template>
    </van-nav-bar>
    <div
        style="background-image: url('https://img0.baidu.com/it/u=3360627435,179419772&fm=253&fmt=auto&app=138&f=JPEG?w=200&h=200')">
      <div id="user-head-group">
        <van-image height="100" width="100" round
                   src="https://img0.baidu.com/it/u=3360627435,179419772&fm=253&fmt=auto&app=138&f=JPEG?w=200&h=200"></van-image>
      </div>
    </div>

    <van-cell-group title="个人信息">
      <van-cell title="用户id" :value="user.id"/>
      <van-cell title="用户名" :value="user.username"/>
      <van-cell title="昵称" :value="user.nickname" is-link/>
      <van-cell title="手机号" value="未绑定" is-link/>
      <van-cell title="邮箱" :value="user.email"/>
      <van-cell title="加入时间" :value="user.create_time.split('T')[0]"/>
    </van-cell-group>

    <van-button type="danger" size="large" v-on:click="logout">退出登录</van-button>
  </div>
</template>

<script>
import {Dialog} from "vant";

export default {
  name: "userPage",
  data() {
    return {
      user: {}
    }
  },
  methods: {
    logout() {
      Dialog.confirm({
        title: "提示",
        message: "确定要退出登录吗？"
      }).then(() => {
        localStorage.clear()
        location.reload()
      }).catch(() => {
        // on cancel
      });

    }
  },
  created() {
    this.user = this.$user
  }
}
</script>

<style scoped>
#user-head-group {
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
}
</style>