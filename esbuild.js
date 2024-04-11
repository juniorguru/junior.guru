import * as esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";

const outdir = process.argv[2];
if (!outdir) {
  console.error("Missing output directory argument");
  process.exit(1);
}

await esbuild.build({
  entryPoints: [
    "project/js/index.js",
    "project/css/index.scss",
    "project/css_legacy/index.scss",
  ],
  bundle: true,
  minify: true,
  sourcemap: true,
  target: "es2020",
  loader: {
    ".svg": "copy",
    ".jpg": "copy",
    ".png": "copy",
    ".webp": "copy",
    ".woff": "copy",
    ".woff2": "copy",
  },
  assetNames: "assets/[name]",
  plugins: [
    sassPlugin({
      // async transform(source) {
      //     const { css } = await postcss([autoprefixer]).process(source);
      //     return css;
      // },
    }),
  ],
  outdir,
});
