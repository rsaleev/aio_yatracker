# AIO Yandex.Tracker Client

## Table of Contents

- [About](#about)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Project is still in development. Main approach to implement all API methods

## Usage <a name = "usage"></a>

```python
import asyncio
from aio_tracker import issues
from aio_tracker.base import TrackerClient

async def main():
    async with BaseClient(os.environ['YANDEX_TOKEN'], os.environ['TRACKER_ORG_ID']) as client:
        issues = await issues.search(client, 'TESTCLIENT') # returns AsyncGenerator
        async for issue in issues: # Pydantic object
            ...
asyncio.run(main())

```
