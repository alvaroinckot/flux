from __future__ import annotations

from examples.tasks.task_rollback import task_rollback
from flux.domain.events import ExecutionEventType
from flux.errors import ExecutionError


def test_should_rollback_and_fail():
    ctx = task_rollback.run()
    assert ctx.has_finished and ctx.has_failed, "The workflow should have failed."

    events = [e.type for e in ctx.events]
    assert ExecutionEventType.WORKFLOW_STARTED in events
    assert ExecutionEventType.TASK_STARTED in events
    assert ExecutionEventType.TASK_ROLLBACK_STARTED in events
    assert ExecutionEventType.TASK_ROLLBACK_COMPLETED in events
    assert ExecutionEventType.TASK_FAILED in events
    assert ExecutionEventType.WORKFLOW_FAILED in events

    return ctx


def test_should_skip_if_finished():
    first_ctx = test_should_rollback_and_fail()
    second_ctx = task_rollback.run(execution_id=first_ctx.execution_id)
    assert first_ctx.execution_id == second_ctx.execution_id
    assert isinstance(first_ctx.output, ExecutionError) and isinstance(
        second_ctx.output,
        ExecutionError,
    )
    assert isinstance(first_ctx.output.inner_exception, ValueError) and isinstance(
        second_ctx.output.inner_exception,
        ValueError,
    )
    assert first_ctx.output.inner_exception.args == second_ctx.output.inner_exception.args
