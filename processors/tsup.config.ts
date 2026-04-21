import {defineConfig} from 'tsup';

export default defineConfig((options) => {
  const isDev = options.env?.NODE_ENV === 'dev';
  return {
    entry: ['src/index.ts'],
    outDir: 'dist',
    sourcemap: true,
    dts: true,
    watch: isDev,
    format: ['cjs', 'esm'],
    ignoreWatch: 'src/test',
  };
});
