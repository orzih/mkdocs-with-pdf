const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const RemoveEmptyScriptsPlugin = require("webpack-remove-empty-scripts")
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
    target: 'es5',

    /* Loaders */
    module: {
      rules: [
        /* Scripts */
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/
        },

        /* SASS stylesheets */
        {
          test: /\.scss$/,
          use: [
            MiniCssExtractPlugin.loader,
            {
              loader: 'css-loader',
              options: {
                url: false,
                sourceMap: true
              }
            },
            {
              loader: 'postcss-loader',
              options: {
                postcssOptions: {
                  plugins: [
                    'autoprefixer',
                    [
                      'postcss-inline-svg',
                      {
                        paths: [path.resolve(__dirname, 'node_modules')],
                        encode: false
                      }
                    ],
                    [
                      'postcss-svgo',
                      {
                        plugins: [
                          { removeDoctype: true },
                          { removeComments: true },
                          { removeDimensions: true },
                          { removeViewBox: false }
                        ],
                        encode: false
                      }
                    ]
                  ],
                  sourceMap: true
                }
              }
            },
            {
              loader: 'sass-loader',
              options: {
                implementation: require('sass'),
                sassOptions: {
                  includePaths: [
                    'node_modules/modularscale-sass/stylesheets',
                    'node_modules/material-design-color'
                  ]
                },
                sourceMap: true
              }
            }
          ]
        }
      ]
    },

    /* Module resolver */
    resolve: {
      modules: [__dirname, path.resolve(__dirname, 'node_modules')],
      extensions: ['.ts', '.js']
    },

    /* Plugins */
    plugins: [],

    /* Source maps */
    devtool: args.mode === 'production' ? 'source-map' : 'eval',

    /* Filter false positives and omit verbosity */
    stats: {
      entrypoints: false
    }
  }
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
        'material-polyfills': 'src/javascripts/index.ts'
      },
      output: {
        path: path.resolve(__dirname, "dist")
      },

      /* Plugins */
      plugins: [
        // ...base.plugins,

        /* Stylesheets */
        new RemoveEmptyScriptsPlugin(),
        new MiniCssExtractPlugin({
          filename: `[name].css`
        })
      ],

      /* Optimizations */
      optimization: {}
    }
  ]
}
