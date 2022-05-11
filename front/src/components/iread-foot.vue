<template>
  <div id="foot-group">
    <div class="foot-btn">按钮</div>
    <div class="foot-btn">按钮</div>
    <div class="foot-btn">按钮</div>
    <div class="foot-btn">按钮</div>
  </div>
</template>

<script>
export default {
  name: "iread-foot",
  props: ["title"]
}
</script>

<style scoped>

#foot-group {
  background-color: red;
  position: fixed;
  bottom: 0;
  display: flex;
  height: 60px;
  width: 100%;
  z-index: 1000;

}

.foot-btn {

}
</style>