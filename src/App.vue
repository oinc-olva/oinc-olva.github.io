<template>
  <Header></Header>
  <router-view />
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>


<style lang="scss">
  @import url('https://fonts.googleapis.com/css2?family=Cedarville+Cursive&family=Schoolbell&display=swap');

  * {
    margin: 0;
    padding: 0;
    font-family: 'Schoolbell', serif;
  }
  .container {
    width: calc(100vw - 20%);
    margin: 0 auto;
  }
</style>
