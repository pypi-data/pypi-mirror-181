const path = require("path");
const webpack = require("webpack");

const HtmlWebpackPlugin = require("html-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");
// const deps = require("./package.json").dependencies;

const shimJS = path.resolve(__dirname, "src", "emptyshim.js");
function shim(regExp) {
  return new webpack.NormalModuleReplacementPlugin(regExp, shimJS);
}

const JUPYTER_HOST = 'http://localhost:8686';

const IS_PRODUCTION = process.argv.indexOf('--mode=production') > -1;
const mode = IS_PRODUCTION ? "production" : "development";
// inline-source-map
const devtool = IS_PRODUCTION ? false : "inline-cheap-source-map";
const minimize = IS_PRODUCTION ? true : false;

module.exports = {
  entry: "./src/Example",
  mode: mode,
  devServer: {
    port: 3063,
    client: { overlay: false },
    historyApiFallback: true,
//    static: path.join(__dirname, "dist"),
    proxy: {
      '/api/jupyter': {
        target: JUPYTER_HOST,
        ws: true,
        secure: false,
        changeOrigin: true,
      },
      '/plotly.js': {
        target: JUPYTER_HOST + '/api/jupyter/pool/react',
        ws: false,
        secure: false,
        changeOrigin: true,
      },
    },
  },
  watchOptions: {
    aggregateTimeout: 300,
    poll: 2000, // Seems to stabilise HMR file change detection
    ignored: "/node_modules/"
  },
  devtool,
  optimization: {
    minimize,
//    usedExports: true,
  },
  output: {
    publicPath: "http://localhost:3063/",
    filename: '[name].[contenthash].datalayerIo.js',
  },
  resolve: {
    extensions: [".ts", ".tsx", ".js", ".jsx"],
    alias: {
      path: "path-browserify",
      stream: "stream-browserify",
    },
  },
  module: {
    rules: [
/*
      {
        test: /bootstrap\.tsx$/,
        loader: "bundle-loader",
        options: {
          lazy: true,
        },
      },
*/
      {
        test: /\.tsx?$/,
        loader: "babel-loader",
        options: {
          plugins: [
            "@babel/plugin-proposal-class-properties",
          ],
          presets: [
            ["@babel/preset-react", {
                runtime: 'automatic',
/*                importSource: '@emotion/react' */
              },
            ],
            "@babel/preset-typescript",
          ],
          cacheDirectory: true
        },
        exclude: /node_modules/,
      },
      {
        test: /\.m?js$/,
        resolve: {
          fullySpecified: false,
        },
      },
      {
        test: /\.jsx?$/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-react"],
          cacheDirectory: true
        }
      },
      {
        test: /\.css?$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        // In .css files, svg is loaded as a data URI.
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        issuer: /\.css$/,
        use: {
          loader: 'svg-url-loader',
          options: { encoding: 'none', limit: 10000 }
        }
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        issuer: /\.tsx$/,
        use: [
          '@svgr/webpack'
        ],
      },
      {
        // In .ts and .tsx files (both of which compile to .js), svg files
        // must be loaded as a raw string instead of data URIs.
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        issuer: /\.js$/,
        use: {
          loader: 'raw-loader'
        }
      },
      {
        test: /\.(png|jpg|jpeg|gif|ttf|woff|woff2|eot)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        use: [{ loader: 'url-loader', options: { limit: 10000 } }],
      },
     ]
  },
  plugins: [
    !IS_PRODUCTION ?
      new webpack.ProvidePlugin({
        process: 'process/browser'
      })
    :
      new webpack.ProvidePlugin({
        process: 'process/browser'
      }),
      new BundleAnalyzerPlugin({
          analyzerMode: IS_PRODUCTION ? "static" : "disabled", // server, static, json, disabled.
          openAnalyzer: false,
          generateStatsFile: false,
        }),
    shim(/@fortawesome/),
    shim(/moment/),
    shim(/react-jvectormap/),
    shim(/react-slick/),
    shim(/react-tagsinput/),
//    shim(/nouislider/),
//    shim(/^codemirror/),
//    shim(/chartist/),
//    shim(/@jupyterlab\/theme-light-extension/),
//    shim(/@jupyterlab\/codeeditor\/lib\/jsoneditor/),
//    shim(/@lumino\/widgets\/lib\/(box|commandpalette|contextmenu|dock|grid|menu|scroll|split|stacked|tab).*/),
//    shim(/@lumino\/collections\/lib\/(bplustree).*/),
//    shim(/@lumino\/(dragdrop|commands).*/),
//    shim(/@jupyterlab\/ui-components/),
//    shim(/@jupyterlab\/apputils\/lib\/(clientsession|dialog|instancetracker|mainareawidget|mainmenu|thememanager|toolbar|widgettracker)/),
//    shim(/@jupyterlab\/apputils\/style\/.*/),
//    shim(/@jupyterlab\/codemirror\/lib\/editor/),
//    shim(/@jupyterlab\/coreutils\/lib\/(time|settingregistry|.*menu.*)/),
//    shim(/@jupyterlab\/services\/lib\/(contents|terminal)\/.*/),
//    shim(/@jupyterlab\/theme-light-extension\/style\/(icons|images)\/.*/),
//    shim(/@jupyterlab\/theme-light-extension\/style\/(urls).css/),
//    shim(/@jupyterlab\/statusbar\/.*/),
    /*
    new ModuleFederationPlugin({
      name: "datalayerIo",
      filename: "datalayerIo.js",
      exposes: {
//        "./routes": "./src/routes",
//        './Io': './src/Io',
      },
      remotes: {
        datalayerWidgets: "datalayerWidgets@http://localhost:3002/datalayerWidgets.js",
//        datalayerUtils: "datalayerUtils@http://localhost:3009/datalayerUtils.js",
//        jupyterSlate: "jupyterSlate@http://localhost:3266/jupyterSlate.js",
//        jupyterReact: "jupyterReact@http://localhost:3208/jupyterReact.js",
      },
      shared: {
//        ...deps,
        react: {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        "react-dom": {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        "react-router-dom": {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        '@mui/material': { 
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        '@mui/system': { 
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        '@mui/styles': { 
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        "@mui/private-theming": {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        '@emotion/core': {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        '@emotion/react': {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
        '@emotion/styled': {
          eager: true,
          singleton: true,
          requiredVersion: false,
        },
      },
    }),
    */
    new HtmlWebpackPlugin({
      template: "./public/index.html",
    }),
  ],
};
