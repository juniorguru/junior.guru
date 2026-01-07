import * as esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";
import postcss from "postcss";
import autoprefixer from "autoprefixer";

const outdir = process.argv[2];
if (!outdir) {
  console.error("Missing output directory argument");
  process.exit(1);
}

await esbuild.build({
  entryPoints: ["src/jg/coop/js/index.js", "src/jg/coop/css/index.scss"],
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
      silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'if-function'],
      async transform(source) {
        const { css } = await postcss([autoprefixer]).process(source, { from: undefined });
        return css;
      },
    }),
  ],
  outdir,
});
