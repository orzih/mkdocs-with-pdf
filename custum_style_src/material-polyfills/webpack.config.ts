import ImageminPlugin from "imagemin-webpack-plugin"
import MiniCssExtractPlugin = require("mini-css-extract-plugin")
import FixStyleOnlyEntriesPlugin = require("webpack-fix-style-only-entries")
import * as path from "path"
import { Configuration } from "webpack"

/* ----------------------------------------------------------------------------
 * Helper functions
 * ------------------------------------------------------------------------- */

/**
 * Webpack base configuration
 *
 * @param args - Command-line arguments
 *
 * @return Webpack configuration
 */
function config(args: Configuration): Configuration {
  return {
    mode: args.mode,

    /* Loaders */
    module: {
      rules: [
        /* SASS stylesheets */
        {
          test: /\.scss$/,
          use: [
            MiniCssExtractPlugin.loader,
            {
              loader: "css-loader",
              options: {
                url: false,
                sourceMap: true,
              },
            },
            {
              loader: "postcss-loader",
              options: {
                postcssOptions: {
                  plugins: [
                    "autoprefixer",
                    ["postcss-inline-svg", {
                      paths: [path.resolve(__dirname, "node_modules")],
                      encode: false,
                    }],
                    ["postcss-svgo", {
                      plugins: [
                        { removeDimensions: true },
                        { removeViewBox: false },
                      ],
                      encode: false,
                    }],
                  ],
                  sourceMap: true,
                },
              },
            },
            {
              loader: "sass-loader",
              options: {
                implementation: require("sass"),
                sassOptions: {
                  includePaths: [
                    "node_modules/modularscale-sass/stylesheets",
                    "node_modules/material-design-color",
                  ],
                },
                sourceMap: true,
              },
            },
          ],
        },
      ],
    },

    /* Module resolver */
    resolve: {
      modules: [__dirname, path.resolve(__dirname, "node_modules")],
    },

    /* Plugins */
    plugins: [],

    /* Source maps */
    devtool: args.mode === "production" ? "source-map" : "eval",

    /* Filter false positives and omit verbosity */
    stats: {
      entrypoints: false,
      warningsFilter: [/export '.[^']+' was not found in/],
    },
  };
}

/* ----------------------------------------------------------------------------
 * Configuration
 * ------------------------------------------------------------------------- */

/**
 * Webpack configuration
 *
 * @param env - Webpack environment arguments
 * @param args - Command-line arguments
 *
 * @return Webpack configurations
 */
export default (_env: never, args: Configuration): Configuration[] => {
  const base = config(args)
  return [
    /* Application */
    {
      ...base,
      entry: {
        "material-polyfills": "src/stylesheets/polyfills.scss"
      },
      output: {
        path: path.resolve(__dirname, "dist")
      },

      /* Plugins */
      plugins: [
        ...base.plugins,

        /* Stylesheets */
        new FixStyleOnlyEntriesPlugin(),
        new MiniCssExtractPlugin({
          filename: `[name].css`
        }),

        /* Minify SVGs */
        new ImageminPlugin({
          svgo: {
            plugins: [{ removeDimensions: true }, { removeViewBox: false }]
          }
        })
      ],

      /* Optimizations */
      optimization: {}
    }
  ]
}
