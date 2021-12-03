<template>
    <section class="notFound">
        <div class="container">
            <h2>De pagina <span class="path">'{{path}}'</span> valt nergens te bespeuren!</h2>
            <p>
                Mogelijks is de originele pagina verwijderd of verplaatst of heeft u een niet-bestaande link geopend. Controleer als u het adres correct hebt ingetoetst en probeer het opnieuw.
            </p>
            <router-link class="link" to="/">Klik hier om terug te keren naar de startpagina</router-link>
        </div>
    </section>
</template>

<script>
export default {
    name: 'Niet Gevonden',
    computed: {
        path() {
            const params = new URLSearchParams(window.location.search)
            return window.location.host + '/' + params.get('p');
        }
    }
}
</script>

<style lang="scss" scoped>
    .notFound {
        background-color: white;
        padding: 50px 0;
    }
    h2 {
        font-weight: normal;
        margin-bottom: 20px;
        font-size: 2em;
        .path { color: gray; }
    }
    p {
        margin-bottom: 20px;
    }
    a {
        color: blue;
        &::before {background-color: blue;}
    }
</style>