<template>
    <footer>
        <div id="footerMain">
            <div class="container">
                <img class="logo" src="/logo.svg" alt="Logo OINC">
                <div id="footerSocialmedia" aria-labelledby="footerSocialmediaTitle">
                    <h1 id="footerSocialmediaTitle">Volg ons op de sociale media</h1>
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
        <span id="copyright">Copyright © 2022-{{new Date().getFullYear()}} &nbsp;|&nbsp; Website gemaakt door Thibo De Vogelaere</span>
        <div id="footerBottomLinks">
            <div class="container">
                <a id="footerOlvaInfo" href="https://olva.be/" target="_blank" aria-label="Website OLVA">
                    <img src="../assets/olva_logo.webp" alt="OLVA logo">
                    <span>OINC is een werkgroep van het Onze-Lieve-Vrouwecollege Assebroek</span>
                </a>
                <a id="footerDisclaimerPrivacy" class="link" href="https://olva.be/privacy/" target="_blank">Disclaimer / Privacy</a>
            </div>
        </div>
    </footer>
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
    footer {
        position: relative;
        background-color: #1b1b1b;
    }
    .container {
        display: flex;
        justify-content: space-between;
    }
    #footerMain {
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
    #footerSocialmedia {
        color: $headingColor;

        h1 {
            font-size: 1.6em;
            margin-bottom: 20px;
        }
        li {
            list-style: none;
            margin: 15px 0 15px 40px;

            a {
                color: $linkColor;
                font-size: 1.2em;

                svg {
                    width: 25px;
                }
                span {
                    margin-left: 20px;
                }
            }
        }
    }
    #copyright {
        display: block;
        color: #979797;
        font-size: .9em;
        text-align: center;
        margin-top: 140px;
        margin-bottom: 30px;
    }

    #footerBottomLinks {
        background-color: #151515;
        padding: 20px 0;
        color: white;

        .container {
            position: relative;
            align-items: center;
            height: 100%;
        }
    }
    #footerOlvaInfo {
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
    #footerDisclaimerPrivacy {
        white-space: nowrap;
        margin-left: 80px;
        color: white;
    }

    @media screen and (max-width: 880px) {
        #footerBottomLinks .container { flex-direction: column; }
        #footerOlvaInfo {
            text-align: center;
            margin-left: 3em;
            img {
                position: absolute;
                top: 50%;
                left: 0;
                transform: translateY(-50%);
            }
        }
        #footerDisclaimerPrivacy {
            margin-top: 20px;
            margin-left: calc(3em + 30px);
        }
    }
    @media screen and (max-width: 840px) {
        #footerMain .container {
            flex-direction: column;

            h1 {
                margin-top: 40px;
                text-align: center;
            }
            li {
                text-align: center;
                margin-left: 0;
            }
        }
    }
    @media screen and (max-width: 540px) {
        #footerOlvaInfo {
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
        #footerDisclaimerPrivacy {
            margin-left: 0;
        }
    }
</style>