<template>
  <div id="viewAbout" class="view">
    <AboutGeneral :content="aboutDesc" /> 
  </div>
</template>

<script>
import AboutGeneral from '../components/about/AboutGeneral'

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