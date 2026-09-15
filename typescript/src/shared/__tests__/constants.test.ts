import {
  ALL_INTERFACES_HOST,
  DEFAULT_HOST,
  LOOPBACK_HOSTNAMES,
  normalizeBindHost,
} from '../constants';

describe('normalizeBindHost', () => {
  it.each(['*', '', '   ', undefined])(
    'translates the "everywhere" shorthand %p into an address the OS can bind',
    (host) => {
      // Node passes the value to dns.lookup(), where a literal `*` fails to
      // resolve and the server never binds at all.
      expect(normalizeBindHost(host)).toBe(ALL_INTERFACES_HOST);
    }
  );

  it.each(['127.0.0.1', '0.0.0.0', '::', 'localhost', '192.168.1.10'])(
    'passes a real address like %s through',
    (host) => {
      expect(normalizeBindHost(host)).toBe(host);
    }
  );

  it('trims surrounding whitespace', () => {
    expect(normalizeBindHost('  127.0.0.1 ')).toBe('127.0.0.1');
  });
});

describe('host defaults', () => {
  it('defaults to loopback, and lists it among the allowed hostnames', () => {
    expect(DEFAULT_HOST).toBe('127.0.0.1');
    expect(LOOPBACK_HOSTNAMES).toEqual(['localhost', '127.0.0.1', '[::1]']);
  });
});
