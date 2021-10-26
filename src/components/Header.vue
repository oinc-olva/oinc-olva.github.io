<template>
    <header>
        <div class="container">
            <div id="logo" :class="{'enlarged': this.page == 'Home'}"><img src="../assets/logo.svg" alt="OINC"></div>
            <nav>
                <ul>
                    <li><router-link to="/">Home</router-link></li>
                    <li><router-link to="/videos">Video's</router-link></li>
                    <li><router-link to="/over-ons">Over ons</router-link></li>
                    <li><router-link to="/contact">Contact</router-link></li>
                </ul>
            </nav>
        </div>
    </header>
</template>

<script>
export default {
    name: 'Header',
    computed: {
        page() { return this.$route.name }
    }
}
</script>

<style lang="scss" scoped>
    @use '../mixins/scrim-gradient.scss' as *;
    $header-height: 60px;

    header {
        position: fixed;
        top: 0; left: 0;
        height: $header-height;
        padding: 40px 0;
        width: 100%;
        z-index: 10;
        filter: drop-shadow(6px 6px 10px rgba(0, 0, 0, 0.1));
        
        &::before {
            content: '';
            display: inline-block;
            position: absolute;
            top: -10px; left: 0;
            width: 100%;
            height: 70%;
            z-index: 1;
            pointer-events: none;
            @include scrimGradient(rgb(31, 31, 31));
        }
    }
    .container {
        display: flex;
    }
    #logo {
        &, img {
            height: #{$header-height * .8};
            transition: transform .2s ease-in-out;
        }
        &.enlarged img {
            transform: translateY(40px) scale(1.3);
        }
    }
    nav, ul, li {
        display: inline-block;
        height: #{$header-height - 20px};
        z-index: 12;
    }
    ul {
        padding-left: 80px;
        line-height: #{$header-height - 20px};
    }
    li {
        list-style: none;
        font-size: 1.1em;
        padding: 0 20px;

        a {
            color: white;
            text-decoration: none;
        }
    }
</style>