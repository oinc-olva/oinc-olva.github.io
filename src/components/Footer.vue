<template>
    <div class="footer">
        <div class="main">
            <div class="container">
                <img class="logo" src="/logo.svg" alt="OINC">
                <div class="socialmedia">
                    <h2>Volg ons op de sociale media</h2>
                    <ul v-if="socialLinks">
                        <li :key="link" v-for="link in socialMedia">
                            <a :href="link.url" :title="link.title" class="link" target="_blank">
                                <fa :icon="['fab', link.name]" v-if="link.iconAvailable" />
                                <fa icon="external-link-alt" rotation="270" v-else />
                                <span>{{link.title}}</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <p class="copyright">Copyright © 2021-{{new Date().getFullYear()}}</p>
        <div class="bottomLinks">
            <div class="container">
                <a class="olva" href="https://olva.be/" target="_blank">
                    <img src="../assets/olva_logo.png" alt="OLVA logo">
                    <span>OINC is een werkgroep van het Onze-Lieve-Vrouwecollege Assebroek</span>
                </a>
                <a class="right link" href="https://olva.be/privacy/" target="_blank">Disclaimer / Privacy</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Footer',
    props: {
        socialLinks: Array
    },
    computed: {
        socialMedia() {
            return this.socialLinks.filter((l) => l.name != 'olva')
        }
    }
}
</script>

<style lang="scss" scoped>
    .footer { background-color: #1b1b1b; }
    .container {
        display: flex;
        justify-content: space-between;
    }
    .main {
        position: relative;
        padding-top: 100px;

        &::before {
            content: '';
            position: absolute;
            display: block;
            top: 0;
            height: 1px;
            width: 100%;
            background: $brandingGradient;
        }
    }
    .logo {
        display: inline-block;
        height: 60px;
    }
    .socialmedia {
        color: #5e6388;

        h2 { padding-bottom: 10px; }
        li {
            list-style: none;
            padding: 5px 0 5px 40px;

            a {
                color: gray;
                font-size: 1.3em;
                &::before { background-color: gray; }

                svg {
                    width: 25px;
                }
                span {
                    padding-left: 20px;
                }
            }
        }
    }
    .copyright {
        color: #777777;
        font-size: .9em;
        text-align: center;
        padding-top: 140px;
        padding-bottom: 30px;
    }

    .bottomLinks {
        background-color: #151515;
        padding: 20px 0;
        color: white;

        .container {
            position: relative;
            align-items: center;
            height: 100%;

            .olva {
                display: flex;
                position: static;
                align-items: center;
                &::before { display: none; }
                &:hover span { color: rgb(153, 153, 153); }

                img {
                    height: 3em;
                }
                span {
                    padding-left: 30px;
                    color: gray;
                }
            }
            .right {
                white-space: nowrap;
                margin-left: 80px;
                color: white;
            }
        }
    }

    @media screen and (max-width: 880px) {
        .bottomLinks .container {
            flex-direction: column;

            .olva {
                text-align: center;
                margin-left: 3em;
                img {
                    position: absolute;
                    top: 50%;
                    left: 0;
                    transform: translateY(-50%);
                }
            }

            .link {
                margin-top: 20px;
                margin-left: calc(3em + 30px);
            }
        }
    }
    @media screen and (max-width: 840px) {
        .main .container {
            flex-direction: column;

            h2 {
                margin-top: 40px;
                text-align: center;
            }
            li {
                text-align: center;
                padding-left: 0;
            }
        }
    }
    @media screen and (max-width: 540px) {
        .bottomLinks .container {
            .olva {
                flex-direction: column;
                margin-left: 0;
    
                span {
                    padding-left: 0;
                    text-align: center;
                }
                img {
                    position: static;
                    margin-bottom: 20px;
                    transform: none;
                }
            }
            .link {
                margin-left: 0;
            }
        }
    }
</style>