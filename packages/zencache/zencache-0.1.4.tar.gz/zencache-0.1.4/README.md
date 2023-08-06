# zencache

Pure memory cache powered by orpc.

## Install

```
pip install zencache
```

## Example server config: zencached-config.yml

```
daemon: true
pidfile: zencached.pid
loglevel: INFO
logfile: zencached.log
server:
  listen: 0.0.0.0
  port: 6779
  backlog: 8192
  buffer_size: 65536
  rfile_buffer_size: 65536
  wfile_buffer_size: 65536
  max_request_size: 4194304
authentication:
  enable: true
  users:
    app01: spnPF3HzY975GJYC
    app02: ZWRVfHrK8QkQoOnQ
    app03: xuFTlTy9i6KCfncp
zencache:
  ttl-scanner-worker-interval: 60
  ttl-scanner-manager-interval: 60
```

## expire options

- NONE: Default option, always set expiry.
- NX: Set expiry only when the key has no expiry.
- XX: Set expiry only when the key has an existing expiry.
- GT: Set expiry only when the new expiry is greater than current one.
- LT: Set expiry only when the new expiry is less than current one.

## Example client usage

```
from orpc_client import OrpcConnectionPool

zencached_client_pool = OrpcConnectionPool(10, kwargs={
    "host": "127.0.0.1",
    "port": 6779,
    "username": "app01",
    "password": "spnPF3HzY975GJYC",
    "login_event": "zencache.login",
    "auto_login": True,
    })

with zencached_client_pool.get_session() as session:
    session.zencache.set('a', 'a')
    assert session.zencache.get('a') == 'a'
```

## Releases

### v0.1.4

- Force to upgrade orpc version.
- Doc update.

### v0.1.3

- Add gevent patch all.
- Force item key to str format.

### v0.1.0

- First release.
