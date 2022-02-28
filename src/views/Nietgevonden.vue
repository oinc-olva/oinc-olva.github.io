<template>
    <section class="notFound view">
        <div class="container">
            <h2>Deze pagina valt nergens te bespeuren!</h2>
            <p>
                Mogelijks is de originele pagina verwijderd of verplaatst of heeft u een niet-bestaande link geopend. Controleer als u het adres correct hebt ingevoerd en probeer het opnieuw.
            </p>
            <div class="home">
                ➤ <router-link class="link" to="/">Klik hier om terug te keren naar de startpagina</router-link>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'Niet Gevonden'
}
</script>

<style lang="scss" scoped>
    .notFound {
        background-color: #2c3141;
        padding: 100px 0;
        color: rgb(170, 170, 170);
    }
    h2 {
        font-size: 2.5em;
        color: #7a81c4;
        margin-bottom: 40px;
    }
    p {
        margin-bottom: 60px;
        color: #9fa3ca;
    }
    .home {
        font-style: italic;
        a { margin-left: 20px; }
    }
</style>