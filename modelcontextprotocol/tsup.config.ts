import {defineConfig} from 'tsup';

export default defineConfig((options) => {
  const isDev = options.env?.NODE_ENV === 'dev';
  return {
    // Named explicitly: globbing `src` also pulled `src/test` into `dist`.
    entry: ['src/cli.ts', 'src/index.ts'],
    outDir: 'dist',
    sourcemap: true,
    watch: isDev,
    // The package is `type: module`, so CJS output would be written as
    // `dist/cli.cjs` and `dev:run`'s `dist/cli.js` would not exist.
    format: ['esm'],
    dts: true,
    ignoreWatch: 'src/test',
  };
});
