import type {Config} from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/test/**/*.test.ts?(x)'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  // Sources carry the explicit .js extensions that ESM requires; jest still
  // resolves the TypeScript sources, so map them back.
  moduleNameMapper: {'^(\\.{1,2}/.*)\\.js$': '$1'},
  setupFilesAfterEnv: ['<rootDir>/src/test/setup.ts'],
};

export default config;
