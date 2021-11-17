<template>
  <div class="about">
    <AboutGeneral :content="aboutDesc" /> 
  </div>
</template>

<script>
import AboutGeneral from '../components/AboutGeneral'

export default {
  name: 'About',
  props: {
    aboutDesc: String
  },
  components: {
    AboutGeneral
  }
}
</script>