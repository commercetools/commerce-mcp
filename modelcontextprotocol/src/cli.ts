#!/usr/bin/env node

/**
 * Executable entry point. Kept separate from `index.ts` so that module's
 * exports stay importable from tests and from other packages without running
 * the server as a side effect.
 */
import {handleError, main} from './index.js';

main().catch((error: unknown) => {
  handleError(error);
  process.exitCode = 1;
});
