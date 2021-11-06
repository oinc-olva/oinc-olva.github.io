<template>
    <div class="footer">
        <div class="main">
            <div class="container">
                <img class="logo" src="../assets/logo.svg" alt="OINC">
                <div class="buffer"></div>
                <div class="socialmedia">
                    <h2>Volg ons op de sociale media</h2>
                    <ul v-if="socialLinks">
                        <li :key="link" v-for="link in socialMedia">
                            <a :href="link.url" target="_blank">
                                <fa :icon="['fab', link.name]" v-if="link.iconAvailable" />
                                <span>{{link.name}}</span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
            <p class="copyright">Copyright © 2021-{{new Date().getFullYear()}}</p>
        </div>
        <div class="bottomLinks">
            <div class="container">
                <a class="olva" href="https://olva.be/" target="_blank">
                    <img src="../assets/olva_logo.png" alt="OLVA logo">
                    <span>OINC is een werkgroep van het Onze-Lieve-Vrouwecollege Assebroek</span>
                </a>
                <div class="buffer"></div>
                <a class="right" href="https://olva.be/privacy/" target="_blank">Disclaimer / Privacy</a>
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
    .main {
        border-top: 4px solid #5e6388;
        padding-top: 100px;
        background-color: #181a20;

        .container {
            display: flex;
        }
    }
    .logo {
        display: inline-block;
        height: 60px;
    }
    .buffer {
        flex: 1;
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

                span {
                    padding-left: 20px;
                }
            }
        }
    }
    .copyright {
        color: #777777;
        text-align: center;
        padding-top: 100px;
        padding-bottom: 30px;
    }

    .bottomLinks {
        $bottomLinksHeight: 100px;
        height: $bottomLinksHeight;
        background-color: #151515;
        color: white;

        &::before {
            content: '';
            display: block;
            height: 1px;
            width: 100%;
            background: linear-gradient(to right, #1c829e 12.5%, #15af46 12.5%, #15af46 25%, #afbe27 25%, #afbe27 37.5%, #fff422 37.5%, #fff422 50%, #f4a636 50%, #f4a636 62.5%, #dc4727 62.5%, #dc4727 75%, #cd2673 75%, #cd2673 87.5%, #917ab6 87.5%, #917ab6 100%);
        }

        .container {
            display: flex;
            align-items: center;
            height: 100%;

            .olva {
                display: flex;
                align-items: center;
                &::before { display: none; }
                &:hover span { color: rgb(153, 153, 153); }

                img {
                    height: #{$bottomLinksHeight * .5};
                }
                span {
                    padding-left: 30px;
                    color: gray;
                }
            }
            .right {
                color: white;
            }
        }
    }
</style>