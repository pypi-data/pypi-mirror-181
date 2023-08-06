# orpc

Open RPC.

## Install

```
pip install orpc
```

## Client Install

```
pip install orpc-client
```

## Protocol

### oRPC request

- request_package = 4bytes-length-byteorder-big + msgstack.dumps(request_body)
- request_body = {"event": "xxx", "args": [], "kwargs": {}}

### oRPC response

- response_package = 4bytes-length-byteorder-big + msgstack.dumps(response_body)
- response_body = {"result": xx, "code": 0, "message": "xxx"}

## simple orpc server usage

### Configs

- server.listen: 0.0.0.0
- server.port 8392
- server.backlog: 8192
- server.buffer_size: 4096
- server.rfile_buffer_size: buffer_size
- server.wfile_buffer_size: buffer_size
- max_request_size: 4194304
- result_packer: zenutils.packutils.RcmPacker
- authentication.enable
- authentication.event
- authentication.users
- services
- enable-debug-service

*More configs see pypi package `daemon-application`.*

- `services` is a list of dict which item contains fields below:
  - `class`: str
  - `args`: list
  - `kwargs`: dict
- `authentication.users` is a username and password dict.
- The `authentication.event` service takes `_protocol_instance` as a keyword parameter.
- Set `_protocol_instance.authenticated` flag to True if login success.
- The `authentication.event` service's password parameter must be given in hash format, e.g. `{SSM3}tcvAvgJqVjqC661OmZewsweDma4AOVaXruOtnCFqZrJoTllTYlNvcw==`, a salted sm3 hash.

### Command Help

```
test@testdeMacBook-Pro orpc % orpc --help
Usage: orpc [OPTIONS] COMMAND [ARGS]...

Options:
  --logfmt TEXT
  --logfile TEXT
  --loglevel TEXT
  --pidfile TEXT          pidfile file path.
  --workspace TEXT        Set running folder
  --daemon / --no-daemon  Run application in background or in foreground.
  -c, --config TEXT       Config file path. Application will search config
                          file if this option is missing. Use sub-command
                          show-config-fileapaths to get the searching tactics.
  --help                  Show this message and exit.

Commands:
  restart                Restart Daemon application.
  show-config-filepaths  Print out the config searching paths.
  show-configs           Print out the final config items.
  start                  Start daemon application.
  stop                   Stop daemon application.
```

## Releases

### v0.1.0

- First release.

### v0.1.2

- Add oRPC connection auto login support.

### v0.1.3

- Add auto_reconnect support for orpc-client.
