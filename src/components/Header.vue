<template>
    <header :class="{burgerMenuOpen: isBurgerMenuOpen, enhanceBackground: isBackgroundEnhanced}">
        <div class="container">
            <div :class="['logo', {'enlarged': this.$route.name == 'Home' && !isBackgroundEnhanced}]">
                <router-link to="/" @click="enterPage" aria-label="Terug naar de startpagina gaan" tabindex="1">
                    <img src="/logo.svg" alt="Logo OINC">
                </router-link>
            </div>
            <button id="burgerMenu" class="icon" @click="$emit('toggleBurgerMenu')" aria-label="Menu">
                <fa :icon="isBurgerMenuOpen ? 'times' : 'bars'" tabindex="1" />
            </button>
            <nav>
                <ul id="headerInternalLinks" aria-label="Pagina's van deze website">
                    <li data-list-item="home"><router-link to="/" @click="enterPage" tabindex="1">Home</router-link></li>
                    <li data-list-item="videos"><router-link to="/videos" @click="enterPage" tabindex="1">Video's</router-link></li>
                    <li data-list-item="over-ons"><router-link to="/over-ons" @click="enterPage" tabindex="1">Over ons</router-link></li>
                </ul>
                <ul id="headerExternalLinks" aria-label="Gerelateerde links">
                    <li :key="link" v-for="link in socialLinks" :aria-label="link.name">
                        <a :href="link.url" :title="link.title" target="_blank" :class="{'olva': link.name == 'olva'}" tabindex="1">
                            <img src="../assets/olva_logo.png" alt="olva" v-if="link.name == 'olva'">
                            <fa :icon="['fab', link.name]" v-else-if="link.iconAvailable" />
                            <span v-else>{{link.title}}</span>
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
        socialLinks: Array,
        isBurgerMenuOpen: Boolean
    },
    emits: [ 'toggleBurgerMenu' ],
    data() {
        return {
            isBackgroundEnhanced: false
        }
    },
    methods: {
        enterPage() {
            if (this.isBurgerMenuOpen) this.$emit('toggleBurgerMenu');
        },
        getHeroHeightPx() {
            let heroHeight = this.$route.meta.heroHeight;
            if (heroHeight == 'vh') return window.innerHeight;
            return heroHeight
        },
        testEnhanceBackground() {
            this.isBackgroundEnhanced = window.scrollY >= this.getHeroHeightPx();
        }
    },
    mounted() {
        document.addEventListener('scroll', this.testEnhanceBackground, false);
    },
    unmounted() {
        document.removeEventListener('scroll', this.testEnhanceBackground, false);
    },
    watch: {
        $route: {
            handler() {
                this.testEnhanceBackground();
            }
        }
    }
}
</script>

<style lang="scss" scoped>
    @use '../mixins/scrim-gradient.scss' as *;
    @use 'sass:math';

    header {
        position: fixed;
        top: 0; left: 0;
        height: $headerSize;
        padding: 40px 0;
        width: 100%;
        pointer-events: none;
        z-index: 10;
        
        &::before {
            content: '';
            display: inline-block;
            position: absolute;
            top: -10px; left: 0;
            width: 100%;
            height: 150%;
            z-index: -2;
            pointer-events: none;
            transition: transform 1s ease-in-out;
            @include scrimGradient(rgba(25, 25, 25, 1));
        }
        &.enhanceBackground::before {
            transform: translateY(25%) scaleY(1.5);
        }

        &.burgerMenuOpen {
            position: fixed;

            nav {
                visibility: visible;
                pointer-events: all;
            }

            #headerInternalLinks li {
                opacity: 1;
                transform: none;
                transition: opacity .3s ease-in-out,
                            transform .3s ease-in-out;

                &[data-list-item=videos] { transition-delay: .1s; }
                &[data-list-item=over-ons] { transition-delay: .2s; }
            }
            #headerExternalLinks {
                opacity: 1;
                transform: translateX(-50%);
            }
        }
    }
    .container {
        position: relative;
        display: flex;
        width: calc(100vw * #{1 - $headerMarginFrac});
        height: 100%;
        align-items: center;
    }
    .logo {
        &, img {
            height: #{$headerSize * .8};
            transition: transform .2s ease-in-out,
                        height .2s ease-in-out;
        }
        &.enlarged { transform: translateY(40px) scale(1.3); }
        a {
            display: block;
            pointer-events: all;
        }
    }
    nav, ul, li {
        display: inline-block;
        z-index: 12;
    }
    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex: 1;
    }
    ul {
        display: flex;
        line-height: #{$headerSize - 20px};
        margin-left: 85px;

        li {
            font-size: 1.1em;

            a { color: white; }
        }
    }

    #headerInternalLinks  a {
        margin: .6em;
        padding: .6em;
        color: rgb(190, 190, 190);
        pointer-events: all;

        &.router-link-active {
            color: white;
            font-weight: bold;
        }
    }
    #headerExternalLinks {
        background-color: rgba(53, 53, 53, 0.2);
        border: 1px solid rgba(143, 143, 143, 0.25);
        border-radius: 40px;
        padding: 5px 10px;
        margin: 0;
        height: #{$headerSize - 20px};
        pointer-events: all;
        transition: opacity .3s ease-in-out,
                    transform .3s ease-in-out,
                    background-color .4s ease-in-out;

        li {
            font-size: #{math.div($headerSize, 2.5)};
            color: white;
            padding: 0 #{math.div($headerSize, 6)};

            /* Voeg een steep toe achter/voor het OLVA logo als het het eerste of laatste element is van de lijst */
            &:first-child .olva {
                margin-right: 10px;
                &::before {
                    content: '';
                    position: absolute;
                    background-color: rgba(143, 143, 143, 0.5);
                    height: 30px;
                    width: 1px;
                    top: 50%;
                    left: 55px;
                    transform: translateY(-50%) rotate(12deg);
                }
            }
            &:last-child .olva {
                margin-left: 10px;
                &::before {
                    content: '';
                    position: absolute;
                    background-color: rgba(143, 143, 143, 0.5);
                    height: 30px;
                    width: 1px;
                    top: 50%;
                    right: 55px;
                    transform: translateY(-50%) rotate(12deg);
                }
            }

            a {
                display: block;
                height: 100%;

                span {
                    display: block;
                    height: 100%;
                    font-size: .5em;
                }

                &.olva {
                    height: #{$headerSize - 20px};

                    img {
                        box-sizing: border-box;
                        height: #{$headerSize - 20px};
                        transform: scale(.8);
                        border: 3px solid rgb(138, 138, 138);
                        border-radius: 50%;
                    }
                }
            }
        }
    }
    #burgerMenu {
        display: none;
        position: absolute;
        right: 0;
        pointer-events: all;
    }

    @media screen and (max-width: 1200px) {
        #headerExternalLinks {
            position: fixed;
            right: calc(100vw * $headerMarginFrac / 2 - 8px);
            opacity: 0;
            pointer-events: none;

            &:focus-within {
                opacity: 1;
                pointer-events: all;
                background: rgb(53, 53, 53);
            }
        }
    }
    @media screen and (max-width: 710px) {
        .logo {
            height: #{$headerSize * .6} !important;
            transform: none !important;

            &, img { height: #{$headerSize * .6} !important; }
        }
        #headerInternalLinks {
            flex: 1;
            margin: 0;
            justify-content: flex-end;

            a { font-size: .9em; }
        }
    }
    @media screen and (max-width: 540px) {
        #headerInternalLinks li[data-list-item=home] { display: none; }
    }
    @media screen and (max-width: 480px) {
        nav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            visibility: hidden;
            pointer-events: none;
            background: rgba(44, 44, 44, 0.9);
            backdrop-filter: saturate(180%) blur(10px);
            z-index: -1;
        }
        #headerInternalLinks {
            flex-direction: column;
            align-items: center;
            font-size: 1.8em;

            li {
                opacity: 0;
                line-height: 250%;
                transform: scale(1.1);
                
                &[data-list-item=home] { display: block; }
            }
        }
        #headerExternalLinks {
            top: calc(100vh - 90px);
            right: unset;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            pointer-events: all;
        }
        #burgerMenu {
            display: inline-block;
        }
    }
</style>