<template>
  <div style="display:flex;height: 100%;width:100%;align-items: center">
    <van-form @submit="onSubmit" style="width: 100%">
      <van-cell-group inset>
        <van-field
            v-model="loginForm.username"
            name="username"
            label="用户名"
            placeholder="用户名"
            :rules="[{ required: true, message: '请填写用户名' }]"
        />
        <van-field
            v-model="loginForm.password"
            type="password"
            name="password"
            label="密码"
            placeholder="密码"
            :rules="[{ required: true, message: '请填写密码' }]"
        />
      </van-cell-group>
      <div style="margin: 16px;">
        <van-button round block type="primary" native-type="submit">
          提交
        </van-button>
        <div style="width: 100%;text-align: right;margin-top: 10px;color: dodgerblue" v-on:click="this.$router.push('/register')">
          没有账号？去注册
        </div>
      </div>
    </van-form>
  </div>
</template>

<script>
import {apiUserLogin} from "@/apis/userApi";
import code from "@/global/code";
import {Toast} from "vant";

export default {
  name: "loginPage",
  data() {
    return {
      "loginForm": {
        "username": "",
        "password": ""
      },
      "user": {}
    }
  },
  methods: {
    onSubmit(values) {
      apiUserLogin({
        "username": values.username,
        "password": values.password,
      }).then(res => {
        if(res.code===code.SUCCESS_CODE){
          this.$user = res.data
          console.log(this.$user)
          localStorage.setItem("user", JSON.stringify(res.data))
          this.$router.push("/home")
        }else {
          Toast.fail(res.msg)
        }
      })
    }
  },
  created() {
    // alert("测试")
  }
}
</script>

<style scoped>

</style>