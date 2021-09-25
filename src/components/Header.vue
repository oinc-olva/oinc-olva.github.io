<template>
    <header>
        <div class="container">
            <h1>OINC</h1>
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
    name: 'Header'
}
</script>

<style lang="scss" scoped>
    @use '../mixins/scrim-gradient.scss' as *;
    @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');
    $header-height: 60px;

    header {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        
        &::before {
            content: '';
            display: inline-block;
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 80px;
            @include scrimGradient(#AAA);
            z-index: -1;
        }
    }
    .container {
        display: flex;
        padding-top: 20px;
    }
    h1, nav, ul, li {
        display: inline-block;
        height: $header-height;
        margin: 0;
        line-height: $header-height;
    }
    h1 {
        display: inline-block;
        font-family: 'Josefin Sans', sans-serif;
        font-size: 4em;
        transform: translateX(-40px) translateY(40px);
    }
    li {
        list-style: none;
        font-size: 1.1em;
        padding: 0 20px;

        a {
            color: black;
            text-decoration: none;
        }
    }
</style>