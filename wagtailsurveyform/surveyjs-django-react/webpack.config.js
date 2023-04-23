const webpack = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");

module.exports = function (env, argv) {
    const options = {mode: argv.mode};
    const isDevBuild = options.mode === "development";

    return {
        mode: options.mode,
        entry: {
            creator: path.resolve(__dirname, "./src/creator.js"),
            dashboard: path.resolve(__dirname, "./src/dashboard.js"),
        },
        resolve: {
            extensions: [".ts", ".js", ".tsx", ".jsx", ".css", ".scss", ".svg"],
        },
        optimization: {
            minimize: !isDevBuild,
        },
        module: {
            rules: [
                {
                    test: /\.(j|t)sx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: "ts-loader",
                        options: {
                            compilerOptions: {},
                        },
                    },
                },
                {
                    test: /\.(s[ac]|c)ss$/i,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                            options: {publicPath: ""},
                        },
                        "css-loader",
                        "postcss-loader",
                        "sass-loader",
                    ],
                },
                {
                    test: /\.jsx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: "babel-loader",
                        options: {
                            presets: [
                                [
                                    "@babel/preset-env",
                                    {
                                        targets: "defaults",
                                        debug: true,
                                        useBuiltIns: "usage",
                                        corejs: 3,
                                    },
                                ],
                                ["@babel/preset-react", {runtime: "automatic"}],
                            ],
                        },
                    },
                },
                {
                    test: /\.(svg|png)$/,
                    use: {
                        loader: "url-loader",
                        options: {},
                    },
                },
            ],
        },
        output: {
            path: path.join(__dirname, "../static/"),
            filename: "js/[name].js",
            library: "SurveyJSDjango",
            libraryTarget: "umd",
            umdNamedDefine: true,
        },
        plugins: [
            new webpack.DefinePlugin({
                "process.env.ENVIRONMENT": JSON.stringify(options.mode),
                // "process.env.VERSION": JSON.stringify(packageJson.version),
            }),
            new MiniCssExtractPlugin({
                filename: "css/[name].css"
            }),
        ],
    };
};
