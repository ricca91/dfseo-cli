"""Generic async task polling module for DataForSEO API.

This module provides reusable polling functionality for async tasks
like On-Page API crawls and Lighthouse audits.
"""

from __future__ import annotations

import sys
import time
from typing import Any, Callable

from dfseo.client import DataForSeoClient, DataForSeoError


def poll_task(
    client: DataForSeoClient,
    task_id: str,
    status_checker: Callable[[DataForSeoClient, str], dict[str, Any]],
    interval: int = 5,
    timeout: int = 300,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
    is_finished: Callable[[dict[str, Any]], bool] | None = None,
) -> dict[str, Any]:
    """Poll an async DataForSEO task until completion or timeout.

    Args:
        client: DataForSEO client instance
        task_id: The task ID to poll
        status_checker: Function that takes (client, task_id) and returns status dict
        interval: Seconds between poll attempts
        timeout: Maximum seconds to wait before raising TimeoutError
        progress_callback: Optional function to call with progress updates
        is_finished: Optional function to check if task is finished (default: checks 'finished' status)

    Returns:
        The final status/result dict from status_checker

    Raises:
        TimeoutError: If timeout is reached before task completes
        DataForSeoError: On API errors
    """
    start_time = time.time()
    elapsed = 0.0

    # Default finished check: status == "finished" or crawl_progress == "finished"
    def _default_is_finished(status: dict[str, Any]) -> bool:
        if status.get("status") == "finished":
            return True
        if status.get("crawl_progress") == "finished":
            return True
        return False

    finished_check = is_finished or _default_is_finished

    while elapsed < timeout:
        # Check current status
        status = status_checker(client, task_id)

        # Build progress info
        progress = _build_progress(status, elapsed)

        # Call progress callback if provided
        if progress_callback:
            progress_callback(progress)

        # Check if finished
        if finished_check(status):
            # Final progress update
            final_progress = _build_progress(status, elapsed, finished=True)
            if progress_callback:
                progress_callback(final_progress)
            return status

        # Wait before next poll
        time.sleep(interval)
        elapsed = time.time() - start_time

    raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")


def _build_progress(
    status: dict[str, Any],
    elapsed: float,
    finished: bool = False,
) -> dict[str, Any]:
    """Build progress dict from status response.

    Args:
        status: Raw status response from API
        elapsed: Elapsed seconds
        finished: Whether the task is finished

    Returns:
        Progress dict for callback/output
    """
    # Extract crawl progress info
    crawl_status = status.get("crawl_status", {})
    pages_crawled = crawl_status.get("pages_crawled", 0)
    pages_in_queue = crawl_status.get("pages_in_queue", 0)

    # Also check top-level fields
    if not pages_crawled:
        pages_crawled = status.get("pages_crawled", 0)
    if not pages_in_queue:
        pages_in_queue = status.get("pages_in_queue", 0)

    progress_status = "finished" if finished else (status.get("crawl_progress", "crawling"))

    return {
        "status": progress_status,
        "pages_crawled": pages_crawled,
        "pages_in_queue": pages_in_queue,
        "elapsed_seconds": int(elapsed),
    }


def print_progress_to_stderr(progress: dict[str, Any]) -> None:
    """Print progress JSON to stderr.

    Args:
        progress: Progress dict with status, pages_crawled, etc.
    """
    import json

    print(json.dumps(progress), file=sys.stderr)


def poll_onpage_task(
    client: DataForSeoClient,
    task_id: str,
    interval: int = 5,
    timeout: int = 300,
    verbose: bool = False,
) -> dict[str, Any]:
    """Poll an On-Page API task until completion.

    This is a convenience function specifically for On-Page API tasks
    that polls the summary endpoint and prints progress to stderr.

    Args:
        client: DataForSEO client instance
        task_id: The task ID to poll
        interval: Seconds between poll attempts
        timeout: Maximum seconds to wait
        verbose: Print verbose status messages

    Returns:
        The summary dict from the API

    Raises:
        TimeoutError: If timeout is reached
        DataForSeoError: On API errors
    """
    def check_summary(client: DataForSeoClient, tid: str) -> dict[str, Any]:
        data = client._request("GET", f"/on_page/summary/{tid}")
        # Extract task result if present
        if data.get("tasks") and len(data["tasks"]) > 0:
            task = data["tasks"][0]
            if task.get("result") and len(task["result"]) > 0:
                return task["result"][0]
        return {}

    def on_progress(progress: dict[str, Any]) -> None:
        print_progress_to_stderr(progress)
        if verbose:
            print(
                f"[poll] status={progress['status']}, "
                f"pages={progress['pages_crawled']}, "
                f"queue={progress['pages_in_queue']}, "
                f"elapsed={progress['elapsed_seconds']}s",
                file=sys.stderr,
            )

    return poll_task(
        client=client,
        task_id=task_id,
        status_checker=check_summary,
        interval=interval,
        timeout=timeout,
        progress_callback=on_progress,
    )


def poll_lighthouse_task(
    client: DataForSeoClient,
    task_id: str,
    interval: int = 5,
    timeout: int = 120,
    verbose: bool = False,
) -> dict[str, Any]:
    """Poll a Lighthouse API task until completion.

    Args:
        client: DataForSEO client instance
        task_id: The task ID to poll
        interval: Seconds between poll attempts
        timeout: Maximum seconds to wait
        verbose: Print verbose status messages

    Returns:
        The Lighthouse result dict from the API

    Raises:
        TimeoutError: If timeout is reached
        DataForSeoError: On API errors
    """
    def check_lighthouse(client: DataForSeoClient, tid: str) -> dict[str, Any]:
        data = client._request("GET", f"/on_page/lighthouse/task_get/json/{tid}")
        # Extract task result if present
        if data.get("tasks") and len(data["tasks"]) > 0:
            task = data["tasks"][0]
            # Lighthouse returns status_code in the task
            status_code = task.get("status_code", 0)
            if status_code == 20000:
                if task.get("result") and len(task["result"]) > 0:
                    result = task["result"][0]
                    # Check if lighthouse result is available
                    if result.get("items") and len(result["items"]) > 0:
                        return {"lighthouse": result["items"][0], "status": "finished"}
            # Task still processing
            return {"status": "processing", "status_code": status_code}
        return {"status": "unknown"}

    def is_lighthouse_finished(status: dict[str, Any]) -> bool:
        return status.get("status") == "finished"

    def on_progress(progress: dict[str, Any]) -> None:
        print_progress_to_stderr(progress)
        if verbose:
            print(
                f"[lighthouse poll] status={progress['status']}, "
                f"elapsed={progress['elapsed_seconds']}s",
                file=sys.stderr,
            )

    return poll_task(
        client=client,
        task_id=task_id,
        status_checker=check_lighthouse,
        interval=interval,
        timeout=timeout,
        progress_callback=on_progress,
        is_finished=is_lighthouse_finished,
    )
