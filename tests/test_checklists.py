from aio_yatracker import checklists
from aio_yatracker.base import BaseClient
import pytest

@pytest.mark.asyncio
async def test_create_checklist(get_client: BaseClient, get_primary_issue_id: str):
    r = await checklists.query.create(
        get_client,
        get_primary_issue_id,
        data=checklists.ChecklistCreateRequest(text="TestChecklistItem"),
    )
    assert isinstance(r, checklists.ChecklistCreateResponse)

@pytest.mark.asyncio
async def test_get_checklist(get_client: BaseClient, get_primary_issue_id: str):
    r = await checklists.query.params(get_client, get_primary_issue_id)
    assert all([isinstance(item, checklists.ChecklistParamsResponse) for item in r])

@pytest.mark.asyncio
async def test_edit_checklist(get_client: BaseClient, get_primary_issue_id: str):
    current = await checklists.query.params(get_client, get_primary_issue_id)
    checkbox = current[0]
    assert isinstance(checkbox, checklists.ChecklistParamsResponse)
    r = await checklists.query.edit(
        get_client,
        get_primary_issue_id,
        checkbox.id,
        data=checklists.ChecklistEditRequest(text="TestEditMethod"),
    )
    assert isinstance(r, checklists.ChecklistEditResponse)

@pytest.mark.asyncio
async def test_delete_checklist_item(get_client: BaseClient, get_primary_issue_id: str):
    created = await checklists.query.create(
        get_client,
        get_primary_issue_id,
        data=checklists.ChecklistCreateRequest(text="TestCheckItemDelete1"),
    )
    for item in created.checklist_items:
        await checklists.query.remove_item(
            get_client,
            get_primary_issue_id,
            checklist_item_id=item.id,
        )

@pytest.mark.asyncio
async def test_delete_checklist(get_client: BaseClient, get_primary_issue_id: str):
    await checklists.query.create(
        get_client,
        get_primary_issue_id,
        data=checklists.ChecklistCreateRequest(text="TestCheckItemDelete1"),
    )
    await checklists.query.remove(get_client, get_primary_issue_id)
