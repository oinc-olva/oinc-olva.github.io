<template>
    <div id="cookieBanner">
        <div id="cookieBannerInnerWrapper">
            <p>
                Wij maken op deze website gebruik van cookies. Een cookie is een eenvoudig klein bestandje dat met pagina's van deze website wordt meegestuurd en door uw browser op uw harde schrijf van uw computer wordt opgeslagen. Wij gebruiken cookies om het gebruik van onze website te optimaliseren. U kunt deze cookies uitzetten via uw browser maar dit kan het functioneren van deze website negatief aantasten.
                <span id="cbLegal">
                    Door op "Akkoord" te klikken ga je akkoord met het <a href="https://olva.be/privacy/" class="link" target="_blank">privacybeleid</a> van het Onze-Lieve-Vrouwecollege Assebroek.
                </span>
            </p>
            <div id="cbConfirmBtn">
                <button class="btn" @click="$emit('confirm')">Akkoord</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CookieBanner',
    emits: [ 'confirm' ]
}
</script>

<style lang="scss" scoped>
    #cookieBanner {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, .4);
        left: 0;
        z-index: 12;
    }
    #cookieBannerInnerWrapper {
        display: flex;
        position: absolute;
        left: 0;
        bottom: 0;
        padding: 20px 60px;
        background: $sectionBackgroundLight;
        border-top: 2px solid $accentColor;
        color: rgb(206, 206, 206);

        #cbLegal {
            display: inline-block;
            margin-top: 10px;
            color: white;

            .link {
                color: $accentColor;
                &::before { background-color: $accentColor; }
            }
        }
        #cbConfirmBtn {
            margin-left: 60px;

            button {
                position: relative;
                top: 50%;
                transform: translateY(-50%);
            }
        }
    }

    @media screen and (max-width: 700px) {
        #cookieBannerInnerWrapper {
            flex-direction: column;
            padding: 40px 40px;

            #cbConfirmBtn {
                margin-top: 30px;
                margin-left: 0;

                button {
                    top: unset;
                    left: 50%;
                    transform: translateX(-50%);
                }
            }
        }
    }
</style>