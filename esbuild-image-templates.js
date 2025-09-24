import { readdir } from "node:fs/promises";
import * as esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";

const outdir = process.argv[2];
if (!outdir) {
  console.error("Missing output directory argument");
  process.exit(1);
}

const result = await esbuild.build({
  entryPoints: (await readdir("src/jg/coop/image_templates"))
    .filter((file) => file.endsWith(".scss"))
    .map((file) => `src/jg/coop/image_templates/${file}`),
  bundle: true,
  minify: true,
  sourcemap: true,
  metafile: true,
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
      precompile(source, pathname) {
        if (pathname.endsWith("@fontsource/inter/index.css")) {
          return source.replaceAll(
            "./files/",
            "../../../../node_modules/@fontsource/inter/files/",
          );
        }
        return source;
      },
    }),
  ],
  outdir,
});

console.log(JSON.stringify(result.metafile, null, 2));
