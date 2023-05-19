# AIO Yandex.Tracker Client

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Project is still in development. Main approach to implement all API methods

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.

## Usage <a name = "usage"></a>

```python
import asyncio
from aio_tracker import issues
from aio_tracker.base import TrackerClient

async def main():
    async with BaseClient(os.environ['YANDEX_TOKEN', 'TRACKER_ORG_ID']) as client:
        issues = await issues.search(client, 'TESTCLIENT') # returns AsyncGenerator
        async for issue in issues: # Pydantic object
            ...
asyncio.run(main())

```
