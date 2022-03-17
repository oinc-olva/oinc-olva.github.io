<template>
    <section id="homeMoreVideos" aria-labelledby="homeMoreVideosTitle">
        <div id="homeMoreVideosTop">
            <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M600,112.77C268.63,112.77,0,65.52,0,7.23V120H1200V7.23C1200,65.52,931.37,112.77,600,112.77Z" class="shape-fill"></path>
            </svg>
        </div>
        <div id="homeMoreVideosContent">
            <div class="container">
                <fa class="h2Icon" :icon="['fab', 'youtube']" />
                <h2 id="homeMoreVideosTitle">Ontdek onze videogallerij!</h2>
                <router-link to="/videos" class="btn">Ontdek</router-link>
            </div>
        </div>
        <div id="homeMoreVideosBottom">
            <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M600,112.77C268.63,112.77,0,65.52,0,7.23V120H1200V7.23C1200,65.52,931.37,112.77,600,112.77Z" class="shape-fill"></path>
            </svg>
        </div>
    </section>
</template>

<script>
export default {
    name: 'HomeMoreVideos'
}
</script>

<style lang="scss" scoped>
    $dividerHeight: 15px;

    #homeMoreVideos {
        position: relative;
        padding-top: $dividerHeight;
        z-index: 1;
    }
    #homeMoreVideosContent {
        position: relative;
        padding: calc(4vw + 30px) 0;
        background-color: $sectionBackgroundLight;

        .container {
            display: flex;
            align-items: center;
            width: calc(100vw * 0.6);

            h2 { flex: 1; }
            a { margin-left: 100px; }
        }
    }
    #homeMoreVideosTop, #homeMoreVideosBottom {
        position: absolute;
        left: 0;
        top: 2px;
        width: 100%;
        overflow: hidden;
        line-height: 0;

        svg {
            position: relative;
            display: block;
            width: calc(100% + 1.3px);
            height: $dividerHeight;

            .shape-fill { fill: $sectionBackgroundLight; }
        }
    }
    #homeMoreVideosBottom {
        top: unset;
        bottom: #{-$dividerHeight + 2px};
        transform: rotate(180deg);
    }

    @media screen and (max-width: 920px) {
        #homeMoreVideosContent .container {
            flex-direction: column;

            svg { display: none; }
            h2 {
                margin: 20px 0 40px;
                text-align: center;
                font-size: calc(2vw + 20px);
            }
            svg, a { margin: 0; }
        }
    }
</style>