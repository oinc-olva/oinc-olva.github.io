<template>
    <header>
        <div class="cutout">
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
    @import url('https://fonts.googleapis.com/css2?family=Short+Stack&display=swap');
    $header-height: 90px;
    $header-background: url('/headerbg.jpg') rgb(255, 255, 255); /* https://creativemarket.com/yemelyanov/4442358-Crumpled-white-paper-background-stock-photo-containing-paper-and-crumpled */ 

    header {
        position: fixed;
        top: 0; left: 0;
        height: $header-height;
        width: 100%;
        filter: drop-shadow(0 6px 2px rgba(0, 0, 0, 0.1));
        
        &::before {
            content: '';
            display: inline-block;
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 30%;
            z-index: 1;
            pointer-events: none;
            @include scrimGradient(rgb(211, 211, 211));
        }
    }
    .cutout {
        background: $header-background;
        $clip-path: polygon(0% 0%, 100% 0%, 100% #{$header-height - 20px}, calc(10% + 14em) #{$header-height - 20px}, calc(10% + 10em) $header-height, 0 $header-height);
        clip-path: $clip-path; -webkit-clip-path: $clip-path;
    }
    .container {
        display: flex;
    }
    nav, ul, li {
        display: inline-block;
        height: #{$header-height - 20px};
        
    }
    ul {
        padding-left: #{$header-height * 2};
        line-height: #{$header-height - 20px};
    }
    h1 {
        display: inline-block;
        font-family: 'Short Stack', sans-serif;
        font-weight: lighter;
        font-size: #{$header-height / 2};
        line-height: #{$header-height + 10px};
        height: $header-height;
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