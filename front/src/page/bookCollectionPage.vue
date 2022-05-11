<template>
  <div style="overflow-x: hidden">

    <div v-if="!isEmpty&&!loadingPage" class="grid">

      <div class="grid-item" v-on:click="bookClick(index)" v-show="item.collect===1"
           v-for="(item,index) in collections" :key="index">
        <van-image radius="10" height="160" width="120" :src="item.book.image_url"
                   style="position: relative">
          <div v-show="isEdit" v-on:click="selected[index]=!selected[index]" class="grid-cover"></div>
          <div v-show="isEdit" class="grid-selected">
            <van-checkbox v-model="selected[index]"/>
          </div>
        </van-image>
        <div class="book-title">{{ item.book.name }}</div>
        <div class="book-tag van-ellipsis" v-show="item.is_read===1">{{ "看到" + item.last_read_chapter }}</div>
        <div class="book-tag" v-show="item.is_read===0">未阅读过该小说</div>
      </div>
    </div>

    <transition name="van-slide-up">
      <div v-show="isEdit" id="foot-group" class="van-hairline--top">
        <div v-on:click="selectAll">
          {{ isSelectAll ? "取消全选" : "全选(已选" + isSelectedNum + "/" + selected.length + ")" }}
        </div>
        <div v-on:click="deleteCollections" style="color: red">删除</div>
      </div>
    </transition>

    <van-empty v-if="isEmpty" description="这里什么都没有(っ °Д °;)っ"/>
  </div>
</template>

<script>
import {Dialog, Toast} from "vant";
import {apiDeleteBookCollections, apiGetBookCollections} from "@/apis/bookApis";


export default {
  name: "bookCollectionPage",
  props: ["isEdit"],
  data() {
    return {
      loadingPage: true,
      collections: [],
      selected: []
    }
  },
  methods: {
    async init() {
      Toast.loading({
        message: "加载数据中...QAQ",
        duration: 0
      })
      this.loadingPage = true
      this.$emit("setEdit", false)
      this.selected = []


      const user_id = this.$user.id
      await apiGetBookCollections({
        user_id: user_id
      }).then(res => {
        this.collections = res.data
        for (let i = 0; i < this.collections.length; i++)
          this.selected.push(false)
      })

      this.loadingPage = false
      Toast.clear()
    },
    bookClick(index){
      if(!this.isEdit)
        this.$router.push('/bookInfo/'+this.collections[index].book.id)
    },
    selectAll() {
      const isSelectAll = this.isSelectAll
      for (let i = 0; i < this.collections.length; i++)
        this.selected[i] = !isSelectAll
    },
    deleteCollections() {
      //删除书架上的书
      if (this.isSelectedNum === 0) {
        Toast.fail("还没有选中的小说")
        return
      }

      Dialog.confirm({
        title: '提示',
        message: '确定要将这些小说从书架中移除吗？',
      }).then(() => {
        const user_id = this.$user.id
        const delete_list = []
        for (let i in this.selected) {
          if (this.selected[i]) delete_list.push(this.collections[i].id)
        }
        console.log(delete_list)
        apiDeleteBookCollections({
          user_id: user_id,
          delete_list: JSON.stringify(delete_list)
        }).then(() => this.init())

      }).catch(() => {
        // on cancel
      });
      Toast.clear()
    }
  },
  computed: {
    isEmpty() {
      return this.collections.length === 0
    },
    isSelectAll() {
      let check = false
      for (let i = 0; i < this.selected.length; i++) {
        if (!this.selected[i]) {
          check = false
          break
        }
      }
      return check
    },
    isSelectedNum() {
      let isSelectedNum = 0
      for (let i = 0; i < this.selected.length; i++) {
        if (this.selected[i])
          isSelectedNum++
      }
      return isSelectedNum
    }
  },
  created() {
    this.init()
  }
}
</script>

<style scoped>
.grid {
  display: flex;
  width: 100%;
  padding: 10px 0 0 0.5%;
  align-items: center;
  flex-wrap: wrap;
}

.grid-cover {
  position: absolute;
  top: 0;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.grid-selected {
  position: absolute;
  background-color: white;
  border-radius: 50px;
  width: 20%;
  height: 0;
  padding-bottom: 20%;
  right: 5%;
  top: 5%;
}

.grid-selected :first-child {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: calc(100vw / 20);
  width: 100%;
  height: 100%;
}

.grid-item {
  width: 31%;
  margin: 5px 1% 5px 1%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.book-title {
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.book-tag {
  /*background-color: linear-gradient(147deg, #FF2525 0%, #e9ef36 74%);*/
  font-size: 10px;
  color: #999;
}

#foot-group {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 50px;
  background-color: white;
  display: flex;
}

#foot-group > div {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 50px;
}
</style>