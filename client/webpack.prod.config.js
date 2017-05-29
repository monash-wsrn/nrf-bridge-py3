/**
 * Created by tanguy on 10/03/17.
 */

let path = require('path');
let webpack = require('webpack');

module.exports = {
    entry: [
        "./src/app.js"
    ],
    module: {
        loaders: [
            {
                test: /\.(jsx|js)?$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            }
        ]
    },
    resolve: {
        extensions: ['.js', '.jsx']
    },
    output: {
        path: path.join(__dirname, "web/static"),
        publicPath: '/static',
        filename: 'app.min.js'
    },
    devServer: {
        contentBase: './web/static',
        hot: false
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env':{
                'NODE_ENV': JSON.stringify('production')
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress:{
                warnings: false
            }
        })
    ]
};
