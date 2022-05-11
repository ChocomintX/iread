<template>
  <div id="headgroup">
    <div id="btn">按钮</div>
    <div id="title">{{ title }}</div>
  </div>
</template>

<script>
export default {
  name: "iread-head",
  props:["title"]
}
</script>

<style scoped>
#headgroup {
  background-color: red;
  width: 100%;
  height: 40px;
  position: fixed;
  top: 0;
  z-index: 1000;
}

#title {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #42b983;
}

#btn {
  position: absolute;
  height: 100%;
  width: 15%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: yellow;
}
</style>