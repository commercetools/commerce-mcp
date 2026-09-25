import {readFileSync} from 'node:fs';
import {join} from 'node:path';
import {SERVER_VERSION} from '../version';

describe('SERVER_VERSION', () => {
  it('matches the published package version', () => {
    // The identity the server reports drifted to 0.4.0 while the package was
    // at 4.1.0 (DEVX-885). This guard fails the build if that happens again.
    const pkg = JSON.parse(
      readFileSync(join(__dirname, '../../../package.json'), 'utf8')
    ) as {version: string};

    expect(SERVER_VERSION).toBe(pkg.version);
  });
});
