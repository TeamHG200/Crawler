var path = require('path');
module.exports = {
    entry: path.resolve(__dirname, './app/main.js'),

    output: {
        filename: path.resolve(__dirname, './static/js/bundle.js')
    },

    module : {
        loaders: [
            {
                test: /\.js$/,
                loader: 'babel',
                exclude: /node_modules/
            },
            {
                test: /\.vue$/,
                loader: 'vue'
            },
            {
                test: /\.css$/,
                loader: "style-loader!css-loader"
            }
        ],
        postLoaders: []
    },


    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.js'
        },
        modulesDirectories: [
            './app/',
            './node_modules/'
        ]
    },

    vue: {
        loaders: {
            js: 'babel'
        }
    },

    babel: {
        presets: ['es2015'],
        plugins: ['transform-runtime']
    }
}
