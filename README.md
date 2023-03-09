# uGPT

uGPT is an API and CLI wrapper for chatGPT and other AIGC API base on [utype](https://github.com/utilmeta/utype) to make integration easier

* Version: `0.1.1` [test]
* Author: [@voidZXL](https://github.com/voidZXL)
* License: MIT

## Features

* provide type-hints for OpenAI's API and enforce them at runtime using [utype](https://github.com/utilmeta/utype), increasing integration experience and reducing bugs
* provide easy to use commands for common AIGC tasks

## Installation

```shell
pip install -U ugpt
```

uGPT requires Python >= 3.7

## CLI Usage
use a simple command to start a chat session with chatGPT
```shell
ugpt chat 
```

**NOTICE**: in the first time, you will be asked for an API key, you can get that in [here](https://platform.openai.com/account/api-keys)

if you need to set a request proxy, you can just use
```shell
ugpt set --proxy=http://127.0.0.1:7890
```

or update your API key using
```shell
ugpt set --key=<YOUR-NEW-API-KEY>
```

### Image generation
you can generate image with prompt in a single command
```shell
ugpt draw "an orca whale in the sea"
```

... more are coming

## API Usage
uGPT provided a developer-friendly wrapper for OpenAI's API, All the API params and responses are type-hinted and enforced at runtime using [utype](https://github.com/utilmeta/utype), increasing integration experience and reduce bugs

such as [image.py](https://github.com/voidZXL/ugpt/blob/main/ugpt/image.py)
