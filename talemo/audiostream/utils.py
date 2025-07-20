# utils.py
from celery import current_task, current_app

def safe_update_state(state: str, task_id: str = None, meta: dict = None):
    """
    Update Celery task state only when we really have a task context.
    This prevents "task_id must not be empty" errors when the helper
    is used outside a running Celery task.

    Args:
        state (str): The state to set for the task
        task_id (str, optional): The ID of the task to update. If not provided,
                                will try to get it from the current task.
        meta (dict, optional): Metadata to include with the state update
    """
    app = current_app

    # If task_id is provided, use it directly
    if task_id:
        app.backend.store_result(task_id, result=None, state=state, meta=meta or {})
        return

    # Otherwise try to get it from the current task context
    task = current_task
    if task and getattr(task.request, "id", None):
        task.update_state(state=state, meta=meta or {})
