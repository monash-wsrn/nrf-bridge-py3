/**
 * Created by tanguy on 06/03/17.
 */

let path = require("path")
let webpack = require("webpack")

module.exports = {
    entry: {
        app: ["./src/app.js"]
    },
    resolve: {
        extensions: ['.js']
    },
    devtool: 'source-map',
    module: {
        rules: [
            { test: /\.js$/, exclude: [/node_modules/, /bin/], loader: "babel-loader" }
        ],
    },
    output: {
        path: path.join(__dirname, "web/static"),
        filename: "app.min.js",
    },
    devServer: {
        contentBase: './web/static',
        hot: true
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ]
};
