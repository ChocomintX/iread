<template>
  <div style="display:flex;height: 100%;width:100%;align-items: center">
    <van-form @submit="onSubmit" style="width: 100%">
      <van-cell-group inset>
        <van-field
            v-model="registerForm.username"
            name="username"
            label="用户名"
            placeholder="用户名"
            :rules="[{ required: true, message: '请填写用户名' }]"
        />
        <van-field
            v-model="registerForm.password"
            type="password"
            name="password"
            label="密码"
            placeholder="密码"
            :rules="[{ required: true, message: '请填写密码' }]"
        />
        <van-field
            v-model="registerForm.rePassword"
            type="password"
            name="rePassword"
            label="确认密码"
            placeholder="再次输入密码"
            :rules="[{ required: true, message: '请确认密码' }]"
        />
        <van-field
            v-model="registerForm.nickName"
            name="nickName"
            label="昵称"
            placeholder="你的昵称"
            :rules="[{ required: true, message: '请输入昵称' }]"
        />
        <van-field
            v-model="registerForm.email"
            name="email"
            type="email"
            label="邮箱"
            placeholder="邮箱"
            :rules="[{ required: true, message: '请填写邮箱' }]"
        />
      </van-cell-group>
      <div style="margin: 16px;">
        <van-button round block type="primary" native-type="submit">
          提交
        </van-button>
      </div>
    </van-form>

  </div>
</template>

<script>
import {apiUserRegister} from "@/apis/userApi";
import {Toast} from "vant";

export default {
  name: "registerPage",
  data() {
    return {
      "registerForm": {
        "username": "",
        "password": "",
        "rePassword": "",
        "nickName": "",
        "email": ""
      },
      "user": {}
    }
  },
  methods: {
    onSubmit(values) {
      apiUserRegister(values).then(res => {
        this.user = res.data
        console.log(res.data)
        if(res.code===0){
          this.$user = res.data
          localStorage.setItem("user", JSON.stringify(res.data))
          this.$router.push("/home")
        }else{
          Toast.fail(res.msg)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>