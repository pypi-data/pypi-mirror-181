# Unimatrix Python SDK

[![PyPI](https://img.shields.io/pypi/v/uni-sdk.svg)](https://pypi.python.org/pypi/uni-sdk) [![Release](https://img.shields.io/github/release/unimtx/uni-python-sdk.svg)](https://github.com/unimtx/uni-python-sdk/releases/latest) [![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/unimtx/uni-python-sdk/blob/main/LICENSE)

The Unimatrix Python SDK provides convenient access to integrate communication capabilities into your Python applications using the Unimatrix HTTP API. The SDK provides support for sending SMS, 2FA verification, and phone number lookup.

## Getting started

Before you begin, you need an [Unimatrix](https://www.unimtx.com/) account. If you don't have one yet, you can [sign up](https://www.unimtx.com/signup?s=python.sdk.gh) for an Unimatrix account and get free credits to get you started.

## Documentation

Check out the documentation at [unimtx.com/docs](https://www.unimtx.com/docs) for a quick overview.

## Installation

Using pip is the recommended way to install the Unimatrix SDK for Python, which is available on [PyPI](https://pypi.org/project/uni-sdk/).

Run the following command to add `uni-sdk` as a dependency to your project:

```bash
pip install uni-sdk
```

## Usage

The following example shows how to use the Unimatrix Python SDK to interact with Unimatrix services.

### Send SMS

Send a text message to a single recipient.

```py

from uni.client import UniClient
from uni.exception import UniException

client = UniClient("your access key id", "your access key secret")

try:
  res = client.messages.send({
    "to": "your phone number", # in E.164 format
    "signature": "your sender name",
    "content": "Your verification code is 2048."
  })
  print(res.data)
except UniException as e:
  print(e)

```

## Reference

### Other Unimatrix SDKs

To find Unimatrix SDKs in other programming languages, check out the list below:

- [Java](https://github.com/unimtx/uni-java-sdk)
- [Go](https://github.com/unimtx/uni-go-sdk)
- [Node.js](https://github.com/unimtx/uni-node-sdk)
- [PHP](https://github.com/unimtx/uni-php-sdk)

## License

This library is released under the [MIT License](https://github.com/unimtx/uni-python-sdk/blob/main/LICENSE).
