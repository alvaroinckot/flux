from __future__ import annotations

from examples.tasks.task_fallback_after_timeout import task_fallback_after_timeout


def test_should_succeed():
    ctx = task_fallback_after_timeout.run()
    assert (
        ctx.has_finished and ctx.has_succeeded
    ), "The workflow should have been completed successfully."
    return ctx


def test_should_skip_if_finished():
    first_ctx = test_should_succeed()
    second_ctx = task_fallback_after_timeout.run(execution_id=first_ctx.execution_id)
    assert first_ctx.execution_id == second_ctx.execution_id
    assert first_ctx.output == second_ctx.output
