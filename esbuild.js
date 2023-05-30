import * as esbuild from 'esbuild'
import { sassPlugin } from "esbuild-sass-plugin";


await esbuild.build({
  entryPoints: [
    "juniorguru/js/index.js",
    'juniorguru/css/index.scss',
    'juniorguru/css_legacy/index.scss',
  ],
  bundle: true,
  minify: true,
  sourcemap: true,
  target: "es2020",
  loader: {
    '.svg': 'copy',
    '.jpg': 'copy',
    '.png': 'copy',
    '.woff': 'copy',
    '.woff2': 'copy',
  },
  assetNames: 'assets/[name]',
  plugins: [
    sassPlugin({
      // async transform(source) {
      //     const { css } = await postcss([autoprefixer]).process(source);
      //     return css;
      // },
    }),
  ],
  outdir: "public/static/",
})
