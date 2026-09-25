// Optional raster export: npm install --no-save --package-lock=false sharp
// node render_images.mjs
import { createRequire } from 'node:module';
import { readdir } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
// SHARP_MODULE is useful in hosts with a bundled renderer; ordinary installs need no override.
const sharp = require(process.env.SHARP_MODULE || 'sharp');
const directory = join(dirname(fileURLToPath(import.meta.url)), 'images');
for (const name of (await readdir(directory)).filter(name => name.endsWith('.svg'))) {
  await sharp(join(directory, name)).png().toFile(join(directory, name.replace(/\.svg$/, '.png')));
}
console.log('Rendered all SVG diagrams to PNG.');
