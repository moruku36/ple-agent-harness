"""Synthetic/mock logging checks, NOT a runtime benchmark or competition score.

No model calls, network connections, real subprocesses, or competition inputs.
"""

import asyncio
import contextlib
import gc
import io
import json
import os
import tempfile
import unittest
from unittest import mock

import harness
import taskbridge


SENTINEL = "SYNTHETIC_TASK_CONTENT_MUST_NOT_APPEAR_IN_LOGS"


class FakeSocket:
  """In-memory protocol transport; never opens a socket."""

  def __init__(self, frames=(), *, error=None, stay_open=False):
    self.frames = list(frames)
    self.error = error
    self.stay_open = stay_open
    self.sent = []

  async def recv(self):
    return json.dumps({"type": "task", "instruction": SENTINEL})

  async def send(self, frame):
    self.sent.append(json.loads(frame))

  def __aiter__(self):
    return self

  async def __anext__(self):
    if self.frames:
      return self.frames.pop(0)
    if self.error is not None:
      raise self.error
    if self.stay_open:
      await asyncio.Future()
    raise StopAsyncIteration


def session_for(ws=None):
  return taskbridge.Session(ws or FakeSocket(), {"instruction": SENTINEL})


def progress_logs(ws):
  return [m["text"] for m in ws.sent if m["type"] == "log"]


class EventLoggingTests(unittest.IsolatedAsyncioTestCase):
  async def test_tool_retry_and_compaction_logs_are_fixed_events(self):
    session = session_for()
    run = harness.Run(session, "synthetic-model")
    for kind in ("tool_execution_start", "auto_retry_start", "compaction_start"):
      await run.on_event({
          "type": kind,
          "toolName": SENTINEL,
          "args": {"command": SENTINEL},
          "error": SENTINEL,
          "message": {"details": SENTINEL},
      })
    self.assertEqual(progress_logs(session.ws), [
        "pi: tool_execution_start", "pi: auto_retry_start", "pi: compaction_start"
    ])

  async def test_model_error_keeps_final_response_and_token_usage(self):
    session = session_for()
    run = harness.Run(session, "synthetic-model")
    await run.on_event({
        "type": "message_end",
        "message": {
            "role": "assistant",
            "content": [{"type": "text", "text": "  " + SENTINEL + "  "}],
            "stopReason": "error",
            "errorMessage": SENTINEL,
            "usage": {"input": 2, "cacheRead": 3, "cacheWrite": 5, "output": 7},
        },
    })
    self.assertEqual(progress_logs(session.ws), ["pi: model_error"])
    self.assertEqual(session.final_message, SENTINEL)
    self.assertEqual(run.replies, 1)
    self.assertEqual(session.ws.sent[-1], {
        "type": "usage", "model": "synthetic-model", "input_tokens": 10,
        "output_tokens": 7, "cache_read_tokens": 3,
    })

  async def test_invalid_and_unknown_stdout_events_are_not_logged(self):
    session = session_for()
    run = harness.Run(session, "synthetic-model")
    for line in (SENTINEL.encode(), b"[]", json.dumps({"type": SENTINEL}).encode()):
      await run.on_line(line)
    self.assertEqual(session.ws.sent, [])


class ProtocolLoggingTests(unittest.IsolatedAsyncioTestCase):
  async def test_malformed_frames_do_not_leak_and_result_dispatch_still_works(self):
    ws = FakeSocket([
        SENTINEL, json.dumps([SENTINEL]),
        json.dumps({"type": "result", "id": "1", "output": SENTINEL}),
        json.dumps({"type": "cancel"}),
    ])
    session = session_for(ws)
    result = asyncio.get_running_loop().create_future()
    pending = asyncio.get_running_loop().create_future()
    session._waiting.update({"1": result, "2": pending})
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
      await session._read()
    with self.assertRaises(taskbridge.Cancelled):
      await pending
    self.assertEqual(stderr.getvalue().splitlines(), [
        "taskbridge: invalid_evaluator_frame", "taskbridge: invalid_evaluator_frame"
    ])
    self.assertEqual(result.result()["output"], SENTINEL)
    self.assertTrue(session.cancelled.is_set())
    self.assertFalse(session._waiting)

  async def test_reader_exception_does_not_leak_and_releases_pending_requests(self):
    # The exception's *type name* is also arbitrary, not safe log metadata.
    failure = type(SENTINEL, (RuntimeError,), {})
    session = session_for(FakeSocket(error=failure(SENTINEL)))
    pending = asyncio.get_running_loop().create_future()
    session._waiting["1"] = pending
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
      await session._read()
    with self.assertRaises(taskbridge.Cancelled):
      await pending
    self.assertEqual(stderr.getvalue().strip(), "taskbridge: evaluator_read_error")
    self.assertTrue(session.cancelled.is_set())

  async def test_success_keeps_final_message(self):
    ws = FakeSocket(stay_open=True)
    handler = mock.AsyncMock(return_value=SENTINEL)
    await taskbridge._session(ws, handler)
    self.assertEqual(ws.sent, [{"type": "done", "final_message": SENTINEL}])

  async def test_handler_failure_without_summary_is_content_free(self):
    ws = FakeSocket(stay_open=True)
    failure = type(SENTINEL, (RuntimeError,), {})
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
      await taskbridge._session(ws, mock.AsyncMock(side_effect=failure(SENTINEL)))
    self.assertEqual(stderr.getvalue().strip(), "taskbridge: harness_error")
    self.assertEqual(ws.sent, [{"type": "error", "message": "harness_error"}])

  async def test_handler_failure_after_summary_keeps_summary_only_in_done(self):
    ws = FakeSocket(stay_open=True)

    async def handler(session):
      session.final_message = SENTINEL
      raise RuntimeError(SENTINEL)

    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
      await taskbridge._session(ws, handler)
    self.assertEqual(stderr.getvalue().strip(), "taskbridge: harness_error")
    self.assertEqual(progress_logs(ws), ["taskbridge: harness_error_after_summary"])
    self.assertEqual(ws.sent[-1], {"type": "done", "final_message": SENTINEL})

  async def test_cancel_keeps_cooperative_final_response(self):
    ws = FakeSocket([json.dumps({"type": "cancel"})])

    async def handler(session):
      await session.cancelled.wait()
      return SENTINEL

    await taskbridge._session(ws, handler)
    self.assertEqual(ws.sent[-1], {"type": "done", "final_message": SENTINEL})
    self.assertEqual(progress_logs(ws), [])

  async def test_relay_tool_errors_remain_protocol_data_not_logs(self):
    session = session_for()
    relay = taskbridge.Relay(session)
    with mock.patch.object(session, "exec", side_effect=taskbridge.TaskError(SENTINEL)):
      status, _, body = await relay._route(
          "POST", f"/{relay.token}/exec", "", {}, b'{"command":"synthetic"}'
      )
    self.assertEqual(status, 200)
    self.assertEqual(json.loads(body), {"ok": False, "error": SENTINEL})
    self.assertEqual(progress_logs(session.ws), [])

  async def test_late_handler_failure_is_not_dumped_by_asyncio(self):
    ws = FakeSocket(stay_open=True)
    started = asyncio.Event()
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()
    errors = []

    async def handler(_session):
      started.set()
      try:
        await asyncio.Future()
      except asyncio.CancelledError:
        raise RuntimeError(SENTINEL) from None

    loop.set_exception_handler(lambda _loop, context: errors.append(context))
    try:
      runner = asyncio.create_task(taskbridge._session(ws, handler))
      await started.wait()
      runner.cancel()
      with self.assertRaises(asyncio.CancelledError):
        await runner
      del runner
      # Let the cancellation handler and exception-retrieval callbacks run,
      # then collect completed tasks to exercise asyncio's fallback logger.
      await asyncio.sleep(0)
      await asyncio.sleep(0)
      gc.collect()
      self.assertEqual(errors, [])
    finally:
      loop.set_exception_handler(previous)


class FakeProcess:
  """Mock process with in-memory streams and a controllable completion event."""

  def __init__(self, stderr, *, ready=True):
    self.stderr = asyncio.StreamReader()
    self.stderr.feed_data(stderr)
    self.stderr.feed_eof()
    self.stdout = asyncio.StreamReader()
    self.stdout.feed_data((SENTINEL + "\n").encode())
    self.stdout.feed_eof()
    self.stdin = mock.Mock(drain=mock.AsyncMock())
    self.returncode = 0 if ready else None
    self.finished = asyncio.Event()
    if ready:
      self.finished.set()

  async def wait(self):
    await self.finished.wait()
    return self.returncode

  async def stop(self, _proc):
    self.returncode = 0
    self.finished.set()


class ProcessLoggingTests(unittest.IsolatedAsyncioTestCase):
  async def test_stderr_is_discarded_not_printed_logged_or_retained(self):
    raw = (SENTINEL + "\n\n" + SENTINEL).encode() + b"\xff"
    proc = FakeProcess(raw)
    session = session_for()
    callback = mock.AsyncMock()
    stderr = io.StringIO()
    with mock.patch.object(asyncio, "create_subprocess_exec", return_value=proc) as create, \
         mock.patch.object(taskbridge, "_stop", side_effect=proc.stop) as stop, \
         contextlib.redirect_stderr(stderr):
      result = await taskbridge.run_process(
          ["synthetic-not-executed"], session, stdin=SENTINEL.encode(),
          on_line=callback, log_prefix=SENTINEL,
      )
    diagnostic = f"taskbridge: subprocess_stderr_discarded bytes={len(raw)}"
    self.assertEqual(stderr.getvalue().strip(), diagnostic)
    self.assertEqual(progress_logs(session.ws), [diagnostic])
    self.assertEqual(result.stderr, "")
    self.assertEqual(result.stderr_bytes, len(raw))
    self.assertEqual(result.code, 0)
    self.assertFalse(result.stopped)
    callback.assert_awaited_once_with(SENTINEL.encode())
    proc.stdin.write.assert_called_once_with(SENTINEL.encode())
    create.assert_awaited_once()
    stop.assert_awaited_once_with(proc)

  async def test_time_budget_still_stops_process_without_dynamic_log_prefix(self):
    proc = FakeProcess(b"", ready=False)
    session = session_for()
    with mock.patch.object(asyncio, "create_subprocess_exec", return_value=proc), \
         mock.patch.object(taskbridge, "_stop", side_effect=proc.stop) as stop, \
         mock.patch.object(session, "time_left", return_value=0):
      result = await taskbridge.run_process(
          ["synthetic-not-executed"], session, log_prefix=SENTINEL
      )
    self.assertEqual(result.code, -1)
    self.assertTrue(result.stopped)
    self.assertEqual(result.stderr, "")
    self.assertEqual(result.stderr_bytes, 0)
    self.assertEqual(progress_logs(session.ws), ["taskbridge: subprocess_deadline_stop"])
    stop.assert_awaited_once_with(proc)

  async def test_task_cancellation_still_cleans_up_process(self):
    proc = FakeProcess(b"", ready=False)
    session = session_for()
    started = asyncio.Event()

    async def create(*_args, **_kwargs):
      started.set()
      return proc

    with mock.patch.object(asyncio, "create_subprocess_exec", side_effect=create), \
         mock.patch.object(taskbridge, "_stop", side_effect=proc.stop) as stop:
      work = asyncio.create_task(taskbridge.run_process(["synthetic-not-executed"], session))
      await started.wait()
      work.cancel()
      with self.assertRaises(asyncio.CancelledError):
        await work
    stop.assert_awaited_once_with(proc)
    self.assertEqual(progress_logs(session.ws), [])

  async def test_stderr_byte_diagnostic_is_capped(self):
    proc = FakeProcess(SENTINEL.encode())
    session = session_for()
    stderr = io.StringIO()
    with mock.patch.object(asyncio, "create_subprocess_exec", return_value=proc), \
         mock.patch.object(taskbridge, "_stop", side_effect=proc.stop), \
         mock.patch.object(taskbridge, "MAX_DIAGNOSTIC_COUNT", 7), \
         contextlib.redirect_stderr(stderr):
      result = await taskbridge.run_process(["synthetic-not-executed"], session)
    self.assertEqual(result.stderr_bytes, 7)
    self.assertEqual(result.stderr, "")
    self.assertEqual(progress_logs(session.ws), [
        "taskbridge: subprocess_stderr_discarded bytes=7"
    ])
    self.assertNotIn(SENTINEL, stderr.getvalue())

  async def test_no_reply_error_does_not_echo_subprocess_stderr(self):
    session = session_for()
    relay = mock.MagicMock()
    relay.env.return_value = {}
    relay.__aenter__.return_value = relay
    # Force a legacy/external Finished carrying raw text to ensure solve does
    # not accidentally start echoing it again. run_process no longer stores it.
    finished = taskbridge.Finished(23, SENTINEL)
    with tempfile.TemporaryDirectory() as scratch, \
         mock.patch.dict(os.environ, {"HOME": scratch}), \
         mock.patch.object(taskbridge, "Relay", return_value=relay), \
         mock.patch.object(harness, "configure", return_value=("google", "synthetic-model")), \
         mock.patch.object(taskbridge, "run_process", return_value=finished):
      with self.assertRaises(RuntimeError) as error:
        await harness.solve(session)
    self.assertNotIn(SENTINEL, str(error.exception))
    self.assertEqual(str(error.exception), "pi: no_assistant_reply exit_code=23")


if __name__ == "__main__":
  unittest.main()
