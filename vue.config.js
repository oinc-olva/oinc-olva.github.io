module.exports = {
    css: {
        loaderOptions: {
            sass: {
                prependData: `
                    @use "@/globalvariables.scss" as *;
                `
            }
        }
    }
}