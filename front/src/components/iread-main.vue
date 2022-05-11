<template>
  <div id="main">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "iread-main"
}
</script>

<style scoped>
#main {
  padding-top: 40px;
  padding-bottom: 60px;
  height: 100%;
  background-color: gray;
}
</style>