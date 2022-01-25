<template>
    <header :class="{burgerMenuOpen: isBurgerMenuOpen}">
        <div class="container">
            <div id="logo" :class="{'enlarged': this.page == 'Home'}" @click="gotoHome"><img src="/logo.svg" alt="OINC"></div>
            <nav>
                <ul class="internalLinks">
                    <li class="home"><router-link to="/" @click="enterPage">Home</router-link></li>
                    <li class="videos"><router-link to="/videos" @click="enterPage">Video's</router-link></li>
                    <li class="over-ons"><router-link to="/over-ons" @click="enterPage">Over ons</router-link></li>
                </ul>
                <ul class="externalLinks">
                    <li :key="link" v-for="link in socialLinks">
                        <a :href="link.url" :title="link.title" target="_blank" :class="{'olva': link.name == 'olva'}">
                            <img src="../assets/olva_logo.png" alt="olva" v-if="link.name == 'olva'">
                            <fa :icon="['fab', link.name]" v-else-if="link.iconAvailable" />
                            <span v-else>{{link.title}}</span>
                        </a>
                    </li>
                </ul>
            </nav>
            <div class="burger" @click="$emit('toggleBurgerMenu')">
                <fa :icon="isBurgerMenuOpen ? 'times' : 'bars'" />
            </div>
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
    computed: {
        page() { return this.$route.name }
    },
    methods: {
        gotoHome() {
            if (this.$router.name !== 'Home') {
                this.$router.push({
                    name: 'Home',
                    path: '/'
                });
            }
        },
        enterPage() {
            if (this.isBurgerMenuOpen) this.$emit('toggleBurgerMenu');
        }
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
            height: 160%;
            z-index: -1;
            pointer-events: none;
            @include scrimGradient(rgba(31, 31, 31, 0.8));
        }

        &.burgerMenuOpen {
            position: fixed;

            nav {
                visibility: visible;
                pointer-events: all;
            }

            .internalLinks li {
                opacity: 1;
                transform: none;
                transition: opacity .3s ease-in-out,
                            transform .3s ease-in-out;

                &.videos { transition-delay: .1s; }
                &.over-ons { transition-delay: .2s; }
            }
            .externalLinks {
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
    #logo {
        &, img {
            height: #{$headerSize * .8};
            transition: transform .2s ease-in-out,
                        height .2s ease-in-out;
        }
        &.enlarged img {
            transform: translateY(40px) scale(1.3);
        }
        &:not(.enlarged) {
            cursor: pointer;
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

            a {
                color: white;
            }
        }

        &.internalLinks a {
            margin: .6em;
            padding: .6em;
        }

        &.externalLinks {
            background-color: rgba(53, 53, 53, 0.2);
            border: 1px solid rgba(143, 143, 143, 0.25);
            border-radius: 40px;
            padding: 5px 10px;
            margin: 0;
            height: #{$headerSize - 20px};
            transition: opacity .3s ease-in-out,
                        transform .3s ease-in-out;

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
    }
    .burger {
        display: none;
        position: absolute;
        color: white;
        right: 0;
        font-size: 20px;
        cursor: pointer;
    }

    @media screen and (max-width: 1200px) {
        .externalLinks {
            position: fixed;
            right: calc(100vw * $headerMarginFrac / 2 - 8px);
            opacity: 0;
            pointer-events: none;
        }
    }
    @media screen and (max-width: 710px) {
        #logo, #logo img {
            height: #{$headerSize * .6} !important;
        }
        #logo img {
            height: #{$headerSize * .6} !important;
            transform: none !important;
        }
        .internalLinks {
            flex: 1;
            margin: 0;
            justify-content: flex-end;

            a {
                font-size: .9em;
            }
        }
    }
    @media screen and (max-width: 540px) {
        .home {
            display: none;
        }
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
            background: rgba(44, 44, 44, 0.5);
            z-index: -1;
        }
        .internalLinks {
            flex-direction: column;
            align-items: center;
            font-size: 1.8em;

            li {
                opacity: 0;
                line-height: 250%;
                transform: scale(1.1);
                
                &.home {
                    display: block;
                }
            }
        }
        .externalLinks {
            top: calc(100vh - 90px);
            right: unset;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            pointer-events: all;
        }
        .burger {
            display: inline-block;
        }
    }
</style>