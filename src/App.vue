<template>
  <Header />
  <Hero />
  <router-view />
</template>

<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'

export default {
  name: 'App',
  components: {
    Header,
    Hero
  }
}
</script>


<style lang="scss">
  @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

  * {
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
  }
  body {
    background-color: black;
    overflow-y: scroll;
  }
  .container {
    width: calc(100vw - 20%);
    margin: 0 auto;
  }
</style>
