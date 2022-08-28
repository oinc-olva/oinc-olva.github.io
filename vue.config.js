const path = require('path');

module.exports = {
    css: {
        loaderOptions: {
            sass: {
                prependData: `
                    @use "@/globalvariables.scss" as *;
                `
            }
        }
    },
    chainWebpack: config => {
        config.plugin('html')
            .tap(args => {
                args[0].template = path.resolve(__dirname, 'public/htmlHeadTags.html')
                return args
            });
        config.plugin('copy')
            .tap(args => {
                args[0].patterns[0].globOptions.ignore.push( path.resolve(__dirname, 'public/htmlHeadTags.html').replace(/\\/g, '/') );
                return args;
            });
    }
}