<template>
    <section id="aboutDesc" aria-label="Info over OINC">
        <div class="container">
            <p>{{content}}</p>
        </div>
    </section>
</template>

<script>
export default {
    name: 'AboutGeneral',
    props: {
        content: String
    }
}
</script>

<style lang="scss" scoped>
    #aboutDesc {
        background-color: #2c3141;
        color: $textColor;
        white-space: pre-wrap;
        padding: 100px 0;
    }
</style>