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
from aiotracker import issues

async def main()
    async with BaseClient(token="<APP TOKEN>", org_id="<TRACKER ORGANIZATION ID>") as client:
        #https://cloud.yandex.com/en/docs/tracker/concepts/issues/search-issues
        async for result in issues.search(client, data=issues.IssueSearchRequest(filter={"queue": "TEST", "assignee": "Empty()"}))
            for issue in result:
            ...

            
asyncio.run(main())

```
