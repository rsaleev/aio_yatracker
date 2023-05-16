from aio_yatracker import issues


async def test_get_issue_parameters(get_client, get_issue_id):
    r = await issues.query.get_issues_parameters(get_client, get_issue_id)
    assert isinstance(r, issues.models.IssueParametersResponse)


async def test_modify_issue(get_client, get_issue_id):
    body = issues.IssueModificationRequest(summary="Test")
    r = await issues.query.edit_issue(
        get_client,
        get_issue_id,
        body,
    )
    assert isinstance(r, issues.models.IssueModificationResponse)
    assert r.summary == "Test"


async def test_create_issue(get_client):
    body = issues.IssueCreationRequest(summary="TestReason", queue="SSTGARBAGE")
    r = await issues.query.create_issue(get_client, body)
    assert isinstance(r, issues.models.IssueCreationResponse)
    assert r.summary == "TestReason"


async def test_move_issue(get_client, get_queue_id):
    created = await issues.query.create_issue(
        get_client,
        issues.IssueCreationRequest(summary="TestReason", queue="TESTCLIENT"),
    )
    assert created
    moved = await issues.query.move_issue(
        get_client, created.id, dest_queue=get_queue_id
    )
    assert moved
    assert moved.queue.key == get_queue_id
    assert moved.previous_queue.key == "TESTCLIENT"


async def test_count_issues(get_client):
    r = await issues.query.count_issues(
        get_client, issues.IssueCountRequest(filter={"queue": "TESTCLIENT"})
    )
    assert r
    assert r > 0


async def test_search_issues(get_client, get_queue_id):
    counter = 1
    async for issues_list in issues.query.search_issues(
        get_client, data=issues.IssueSearchRequest(filter={"queue": get_queue_id})
    ):
        assert issues_list
        assert all([issue.queue.key == get_queue_id for issue in issues_list])
        counter += 1
    assert counter > 1
