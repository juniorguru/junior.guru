import { readdir } from 'node:fs/promises';
import * as esbuild from 'esbuild'
import { sassPlugin } from 'esbuild-sass-plugin';

const outdir = process.argv[2];
if (!outdir) {
  console.error('Missing output directory argument');
  process.exit(1);
}

await esbuild.build({
  entryPoints: (await readdir('juniorguru/image_templates'))
    .filter(file => file.endsWith('.scss'))
    .map(file => `juniorguru/image_templates/${file}`),
  bundle: true,
  minify: true,
  sourcemap: true,
  target: "es2020",
  loader: {
    '.svg': 'copy',
    '.jpg': 'copy',
    '.png': 'copy',
    '.webp': 'copy',
    '.woff': 'copy',
    '.woff2': 'copy',
  },
  assetNames: 'assets/[name]',
  plugins: [
    sassPlugin(),
  ],
  outdir,
})
