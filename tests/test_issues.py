from aio_yatracker import issues
from aio_yatracker.common import Relationship


async def test_get_issue_parameters(get_client, get_primary_issue_id):
    r = await issues.query.params(get_client, get_primary_issue_id)
    assert isinstance(r, issues.models.IssueParametersResponse)


async def test_modify_issue(get_client, get_primary_issue_id):
    body = issues.IssueModificationRequest(summary="Test")
    r = await issues.query.modify(
        get_client,
        get_primary_issue_id,
        body,
    )
    assert isinstance(r, issues.models.IssueModificationResponse)
    assert r.summary == "Test"


async def test_create_issue(get_client, get_primary_queue_id):
    body = issues.IssueCreationRequest(summary="TestReason", queue=get_primary_queue_id)
    r = await issues.query.create(get_client, body)
    assert isinstance(r, issues.models.IssueCreationResponse)
    assert r.summary == "TestReason"


async def test_move_issue(get_client, get_primary_queue_id, get_secondary_queue_id):
    created = await issues.query.create(
        get_client,
        issues.IssueCreationRequest(summary="TestReason", queue=get_primary_queue_id),
    )
    assert created
    moved = await issues.query.move(
        get_client,
        created.id,
        dest_queue=get_secondary_queue_id,
        expand=True,
        expand_attachments=True,
    )
    assert moved
    assert moved.queue.key == get_secondary_queue_id
    assert moved.previous_queue.key == get_primary_queue_id


async def test_count_issues(get_client, get_primary_queue_id):
    r = await issues.query.count(
        get_client, issues.IssueCountRequest(filter={"queue": get_primary_queue_id})
    )
    assert r
    assert r > 0


async def test_search_issues(get_client, get_primary_queue_id):
    async for issues_list in issues.query.search(
        get_client,
        data=issues.IssueSearchRequest(filter={"queue": get_primary_queue_id}),
    ):
        assert all(
            isinstance(issue, issues.IssueSearchResponse) for issue in issues_list
        )
        assert all([issue.queue.key == get_primary_queue_id for issue in issues_list])


async def test_priorities(get_client):
    async for priorities_list in issues.query.priorities(get_client):
        assert all(
            isinstance(priority, issues.IssuePrioritiesResponse)
            for priority in priorities_list
        )


async def test_transitions(get_client, get_primary_issue_id):
    async for transitions_list in issues.query.transitions(
        get_client, get_primary_issue_id
    ):
        assert all(
            isinstance(transition, issues.IssueTransitionResponse)
            for transition in transitions_list
        )


async def test_changelog(get_client, get_secondary_issue_id):
    r = await issues.query.changelog(get_client, get_secondary_issue_id)
    assert all([isinstance(changes, issues.IssueChangelogResponse) for changes in r])


async def test_link_create(get_client, get_primary_issue_id, get_secondary_issue_id):
    data = issues.IssueRelationshipCreateRequest(
        relationship=Relationship.RELATES, issue=get_secondary_issue_id
    )
    r = await issues.query.link(get_client, get_primary_issue_id, data=data)
    assert isinstance(r, issues.IssueRelationshipCreateResponse)


async def test_links(get_client, get_primary_issue_id):
    r = await issues.query.links(get_client, get_primary_issue_id)
    assert all([isinstance(item, issues.IssueRelationshipResponse) for item in r])

async def test_link_remove(get_client, get_primary_issue_id, get_secondary_issue_id):
    current_links = await issues.query.links(get_client, get_primary_issue_id)
    link_id = next(link.id for link in current_links if link.object.key == get_secondary_issue_id)
    await issues.query.remove_link(
        get_client, get_primary_issue_id, link_id
    )



