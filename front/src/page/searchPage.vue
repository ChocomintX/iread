<template>
  <div>
    <van-sticky z-index="45">
      <div id="head-group">

        <!--      <van-search-->
        <!--          placeholder="搜索作品名"-->
        <!--          readonly-->
        <!--          :style="{height:'100%',flexGrow:1}"-->
        <!--          v-on:click="this.$router.push('/search')"-->
        <!--      >-->
        <!--        <template #action>-->
        <!--          <div @click="onClickButton">搜索</div>-->
        <!--        </template>-->
        <!--      </van-search>-->

        <van-search
            v-model="searchText"
            show-action
            left-icon="arrow-down"
            :style="{height:'100%',flexGrow:1}"
            placeholder="请输入搜索关键词"
            @search="onSearch"
            @cancel="this.$router.back()"
        >

          <template #label>
            <div @click="onClickButton" @click.prevent>{{ type[pickType].text }}</div>
          </template>
          <template #left-icon>
            <van-icon name="arrow-down" @click="onClickButton"/>
          </template>
        </van-search>
      </div>
    </van-sticky>
    <div v-show="!isSearch" style="margin-left: 5px">
      <div style="margin: 10px 0 0 10px;color: #999999;font-size: 12px">搜索历史</div>
      <div id="search-history-group">
        <van-tag v-for="index in 10" :key="index" :show="show[index]" color="rgba(0,0,0,0.1)" text-color="black"
                 class="search-history-item" closeable size="medium" type="primary" @close="show[index]=false">
          标签{{ index }}
        </van-tag>
      </div>
    </div>
    <van-popup v-model:show="showPicker" position="bottom">
      <van-picker
          :columns="type"
          title="选择搜索类型"
          @confirm="selectType"
          @cancel="showPicker = false"
      />
    </van-popup>
    <manga-search-page v-if="isSearch" :search-count="searchCount" :keywords="searchText"></manga-search-page>
  </div>
</template>

<script>
import MangaSearchPage from "@/page/mangaSearchPage";

export default {
  name: "searchPage",
  components: {MangaSearchPage},
  data() {
    return {
      searchText: "",
      showPicker: false,
      isSearch: false,
      searchCount:0,
      type: [{text: "漫画"}, {text: "小说", disabled: false}],
      pickType: 0,
      show: [true, true, true, true, true, true, true, true, true, true],
      showSearch:false
    }
  },
  methods: {
    onClickButton() {
      this.showPicker = true
    },
    onSearch() {
      this.isSearch = true
      this.searchCount++
    },
    selectType(value, index) {
      console.log(`当前值：${value}, 当前索引：${index}`)
      this.pickType = index
      this.showPicker = false
    },
  }
}
</script>

<style scoped>
#head-group {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;

  background-color: white;
}

#search-history-group {
  display: flex;
  flex-wrap: wrap;
}

.search-history-item {
  padding: 5px 8px 5px 10px;
  margin: 10px 0 0 10px;
  font-size: 10px;
  border-radius: 5px;
}
</style>