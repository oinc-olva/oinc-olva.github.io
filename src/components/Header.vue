<template>
    <header>
        <div class="container">
            <div id="logo" :class="{'enlarged': this.page == 'Home'}"><img src="../assets/logo.svg" alt="OINC"></div>
            <nav>
                <ul class="internalLinks">
                    <li><router-link to="/">Home</router-link></li>
                    <li><router-link to="/videos">Video's</router-link></li>
                    <li><router-link to="/over-ons">Over ons</router-link></li>
                </ul>
                <ul class="externalLinks">
                    <li :key="link" v-for="link in socialLinks">
                        <a :href="link.url" :title="link.name" target="_blank" :class="{'olva': link.name == 'olva'}">
                            <img src="../assets/olva_logo.png" alt="olva" v-if="link.name == 'olva'">
                            <fa :icon="['fab', link.name]" v-else-if="link.iconAvailable" />
                            <span v-else>{{link.name}}</span>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    </header>
</template>

<script>
export default {
    name: 'Header',
    props: {
        socialLinks: Array
    },
    computed: {
        page() { return this.$route.name }
    }
}
</script>

<style lang="scss" scoped>
    @use '../mixins/scrim-gradient.scss' as *;
    @use 'sass:math';

    header {
        position: absolute;
        top: 0; left: 0;
        height: $headerSize;
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
            height: 90%;
            z-index: -1;
            pointer-events: none;
            @include scrimGradient(rgb(39, 39, 39));
        }
    }
    .container {
        display: flex;
        width: calc(100vw * #{1 - $headerMarginFrac});
    }
    #logo {
        &, img {
            height: #{$headerSize * .8};
            transition: transform .2s ease-in-out;
        }
        &.enlarged img {
            transform: translateY(40px) scale(1.3);
        }
    }
    nav, ul, li {
        display: inline-block;
        height: #{$headerSize - 20px};
        z-index: 12;
    }
    nav {
        display: flex;
        justify-content: space-between;
        flex: 1;
    }
    ul {
        margin-left: 80px;
        line-height: #{$headerSize - 20px};

        li {
            list-style: none;
            font-size: 1.1em;
            padding: 0 20px;

            a {
                color: white;
            }
        }

        &.externalLinks {
            display: flex;
            background-color: rgba(53, 53, 53, 0.2);
            border: 1px solid rgba(143, 143, 143, 0.25);
            border-radius: 40px;
            padding: 5px 10px;

            li {
                font-size: #{math.div($headerSize, 2.5)};
                color: white;
                padding: 0 #{math.div($headerSize, 6)};

                a {
                    display: block;
                    height: 100%;

                    &.olva {
                        img {
                            box-sizing: border-box;
                            height: 100%;
                            transform: scale(.8);
                            border: 3px solid rgb(138, 138, 138);
                            border-radius: 50%;
                        }
                    }
                }
                
            }
        }
    }
</style>