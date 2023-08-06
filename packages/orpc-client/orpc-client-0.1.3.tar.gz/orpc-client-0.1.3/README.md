# orpc-client

Open RPC client.

## Install

```
pip install orpc-client
```

## Server Install

```
pip install orpc
```

## About Connection Login sm3utils deps

For most newly installed python, `sm3 hash method` is already provided. If your python installation doesn't support `sm3 hash method`, you need to install it via `pip install sm3utils` by yourself.

## Protocol

### oRPC request

- request_package = 4bytes-length-byteorder-big + msgstack.dumps(request_body)
- request_body = {"event": "xxx", "args": [], "kwargs": {}}

### oRPC response

- response_package = 4bytes-length-byteorder-big + msgstack.dumps(response_body)
- response_body = {"result": xx, "code": 0, "message": "xxx"}

## Releases

### v0.1.0

- First release.

### v0.1.2

- Add oRPC connection auto login support.

## v0.1.3

- Add auto_reconnect support for orpc-client.
