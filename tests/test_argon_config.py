"""Local generated-config/CLI checks, NOT model request or runtime validation.

No credentials, network, Pi process, model/judge calls, or competition inputs.
"""

import json
import os
import pathlib
import tempfile
import types
import unittest
from unittest import mock

import harness
import taskbridge


ARGON = "gemini-4-argon"
NATIVE_ENV = {
    "MODEL_NAME": ARGON,
    "GOOGLE_GEMINI_BASE_URL": "https://synthetic.invalid/gemini",
}
COMPATIBLE_ENV = {
    "MODEL_NAME": ARGON,
    "MODEL_BASE_URL": "https://synthetic.invalid/openai/v1",
}
SAFE_FLAGS = {
    "GOOGLE_GENAI_USE_ENTERPRISE": "false",
    "GOOGLE_GENAI_USE_VERTEXAI": "false",
}
REJECTED_FLAG = "pi: native_google_cloud_backend_flag_rejected"


def fake_relay(env=None):
  """Never binds a listener or opens a connection."""
  relay = mock.MagicMock()
  relay.env.side_effect = lambda: dict(os.environ) if env is None else env
  relay.mcp_url.side_effect = lambda name: f"http://synthetic.invalid/mcp/{name}"
  relay.__aenter__.return_value = relay
  return relay


class ConfigurationTests(unittest.TestCase):
  def configure_for(self, env, *, catalog=False):
    session = types.SimpleNamespace(mcp_servers=[{"name": "synthetic"}])
    with tempfile.TemporaryDirectory() as scratch, \
         mock.patch.dict(os.environ, env, clear=True), \
         mock.patch.object(harness, "in_catalog", return_value=catalog) as probe, \
         mock.patch.object(harness.subprocess, "run", side_effect=AssertionError(
             "A configuration test must not create a subprocess"
         )):
      agent_dir = pathlib.Path(scratch)
      inherited = dict(os.environ)
      child_env = {}
      selected = harness.configure(agent_dir, fake_relay(), session, child_env)
      expected_env = SAFE_FLAGS if selected[0] == "google" else {}
      probe.assert_called_once_with(selected[0], env["MODEL_NAME"], expected_env)
      self.assertIsNot(probe.call_args.args[2], child_env)
      self.assertEqual(child_env, {})
      self.assertEqual(dict(os.environ), inherited)
      return selected, {
          name: json.loads((agent_dir / name).read_text())
          for name in ("models.json", "settings.json", "mcp.json")
      }

  def assert_argon_fallback(self, config):
    self.assertEqual(config["models"], [{
        "id": ARGON,
        "name": ARGON,
        "input": ["text", "image"],
        "contextWindow": 1048576,
        "maxTokens": 65536,
    }])
    # This assertion is about models.json, not Pi's serialized API request.
    self.assertNotIn("reasoning", config["models"][0])
    self.assertNotIn("thinkingBudget", config["models"][0])

  def test_submission_declares_argon(self):
    # The declaration is a simple scalar; no YAML dependency is needed.
    declarations = [
        line.strip() for line in (harness.HERE / "submission.yaml").read_text().splitlines()
        if line.startswith("model_api:")
    ]
    self.assertEqual(declarations, ["model_api: google-cloud/gemini-4-argon"])

  def test_native_argon_uses_specific_text_image_limits(self):
    selected, files = self.configure_for(NATIVE_ENV)
    self.assertEqual(selected, ("google", ARGON))
    config = files["models.json"]["providers"]["google"]
    self.assertEqual(config["baseUrl"], "https://synthetic.invalid/gemini/v1beta")
    self.assertEqual(config["api"], "google-generative-ai")
    self.assertEqual(config["apiKey"], "$GEMINI_API_KEY")
    self.assert_argon_fallback(config)
    self.assertEqual(files["settings.json"]["defaultProjectTrust"], "never")
    self.assertEqual(files["settings.json"]["cacheWarming"], "off")
    self.assertEqual(files["mcp.json"], {"mcpServers": {"synthetic": {
        "url": "http://synthetic.invalid/mcp/synthetic", "timeout": 300,
    }}})

  def test_compatible_argon_uses_same_fallback_without_changing_route(self):
    selected, files = self.configure_for(COMPATIBLE_ENV)
    self.assertEqual(selected, ("model", ARGON))
    config = files["models.json"]["providers"]["model"]
    self.assertEqual(config["baseUrl"], COMPATIBLE_ENV["MODEL_BASE_URL"])
    self.assertEqual(config["api"], "openai-completions")
    self.assertEqual(config["apiKey"], "$MODEL_API_KEY")
    self.assert_argon_fallback(config)

  def test_other_uncatalogued_models_keep_generic_limits(self):
    for route in (NATIVE_ENV, COMPATIBLE_ENV):
      with self.subTest(route=route):
        env = {**route, "MODEL_NAME": "synthetic-other-model"}
        selected, files = self.configure_for(env)
        config = files["models.json"]["providers"][selected[0]]
        self.assertEqual(config["models"], [{
            "id": "synthetic-other-model", "name": "synthetic-other-model",
            "input": ["text"], "contextWindow": 128000, "maxTokens": 16384,
        }])

  def test_catalogued_other_model_keeps_provider_catalog_behavior(self):
    env = {
        "MODEL_NAME": "synthetic-catalogued-model",
        "ANTHROPIC_BASE_URL": "https://synthetic.invalid/anthropic",
    }
    selected, files = self.configure_for(env, catalog=True)
    self.assertEqual(selected, ("anthropic", "synthetic-catalogued-model"))
    config = files["models.json"]["providers"]["anthropic"]
    self.assertNotIn("models", config)
    self.assertEqual(config["api"], "anthropic-messages")
    self.assertEqual(config["compat"], harness.COMPAT)

  def test_native_configure_rejects_unsafe_parent_or_child_before_catalog(self):
    session = types.SimpleNamespace(mcp_servers=[])
    for flag in SAFE_FLAGS:
      # A safe value in one environment must not mask an unsafe other source.
      for inherited, child in (
          ({flag: "true"}, SAFE_FLAGS),
          (SAFE_FLAGS, {flag: "SYNTHETIC_VALUE_MUST_NOT_LEAK"}),
      ):
        with self.subTest(flag=flag, inherited=inherited), \
             tempfile.TemporaryDirectory() as scratch, \
             mock.patch.dict(os.environ, {**NATIVE_ENV, **inherited}, clear=True), \
             mock.patch.object(harness, "in_catalog") as probe, \
             mock.patch.object(harness.subprocess, "run", side_effect=AssertionError(
                 "A guard test must not create a subprocess"
             )) as raw_process:
          before = dict(os.environ)
          child_before = dict(child)
          with self.assertRaises(RuntimeError) as error:
            harness.configure(pathlib.Path(scratch), fake_relay(), session, child)
          self.assertEqual(str(error.exception), REJECTED_FLAG)
          probe.assert_not_called()
          raw_process.assert_not_called()
          self.assertEqual(list(pathlib.Path(scratch).iterdir()), [])
          self.assertEqual(dict(os.environ), before)
          self.assertEqual(child, child_before)


class CliSelectionTests(unittest.IsolatedAsyncioTestCase):
  async def solve_for(self, model_env, *, relay_env=None, rejected=False):
    session = types.SimpleNamespace(
        workdir="/synthetic", instruction="Synthetic task only.",
        mcp_servers=[], final_message="", usage=mock.AsyncMock(),
    )
    captured = {}

    async def run_process(argv, received_session, **kwargs):
      captured["argv"] = argv
      captured["env"] = dict(kwargs["env"])
      captured["models"] = json.loads(
          (pathlib.Path(kwargs["env"]["PI_CODING_AGENT_DIR"]) / "models.json").read_text()
      )
      self.assertIs(received_session, session)
      self.assertEqual(kwargs["stdin"], b"Synthetic task only.")
      await kwargs["on_line"](json.dumps({
          "type": "message_end",
          "message": {
              "role": "assistant",
              "content": [{"type": "text", "text": "Synthetic completion."}],
          },
      }).encode())
      return taskbridge.Finished(0, "")

    with tempfile.TemporaryDirectory() as scratch, \
         mock.patch.dict(os.environ, {**model_env, "HOME": scratch}, clear=True), \
         mock.patch.object(taskbridge, "Relay", return_value=fake_relay(relay_env)), \
         mock.patch.object(harness, "in_catalog", return_value=False) as probe, \
         mock.patch.object(harness.subprocess, "run", side_effect=AssertionError(
             "A CLI test must not create a subprocess"
         )) as raw_process, \
         mock.patch.object(taskbridge, "run_process", side_effect=run_process) as process:
      before = dict(os.environ)
      relay_before = None if relay_env is None else dict(relay_env)
      if rejected:
        with self.assertRaises(RuntimeError) as error:
          await harness.solve(session)
        self.assertEqual(str(error.exception), REJECTED_FLAG)
        probe.assert_not_called()
        process.assert_not_called()
      else:
        result = await harness.solve(session)
        self.assertEqual(result, "Synthetic completion.")
        process.assert_awaited_once()
        probe.assert_called_once()
        self.assertEqual(probe.call_args.args[2], captured["env"])
      raw_process.assert_not_called()
      self.assertEqual(dict(os.environ), before)
      self.assertEqual(relay_env, relay_before)
    return captured

  async def test_argon_cli_selects_high_on_both_routes(self):
    for env, provider in ((NATIVE_ENV, "google"), (COMPATIBLE_ENV, "model")):
      with self.subTest(provider=provider):
        captured = await self.solve_for(env)
        argv = captured["argv"]
        self.assertEqual(argv[argv.index("--provider") + 1], provider)
        self.assertEqual(argv[argv.index("--model") + 1], ARGON)
        self.assertEqual(argv[argv.index("--thinking") + 1], "high")
        config = captured["models"]["providers"][provider]["models"][0]
        self.assertEqual(config["input"], ["text", "image"])
        self.assertNotIn("reasoning", config)
        self.assertNotIn("thinkingBudget", config)

  async def test_other_model_keeps_max_cli_default(self):
    captured = await self.solve_for({**NATIVE_ENV, "MODEL_NAME": "synthetic-other-model"})
    argv = captured["argv"]
    self.assertEqual(argv[argv.index("--thinking") + 1], "max")

  async def test_native_missing_or_exact_false_flags_get_safe_child_copy(self):
    for flags in ({}, *({flag: "false"} for flag in SAFE_FLAGS), SAFE_FLAGS):
      with self.subTest(flags=flags):
        captured = await self.solve_for({**NATIVE_ENV, **flags}, relay_env=dict(flags))
        self.assertEqual({flag: captured["env"][flag] for flag in SAFE_FLAGS}, SAFE_FLAGS)

  async def test_native_unsafe_flags_fail_before_catalog_and_process(self):
    values = ("true", "TRUE", "1", "yes", "", "False", "FALSE", "0",
              " false", "false\n", "SYNTHETIC_VALUE_MUST_NOT_LEAK")
    for flag in SAFE_FLAGS:
      for value in values:
        with self.subTest(flag=flag, value=value):
          await self.solve_for({**NATIVE_ENV, flag: value}, rejected=True)
      for inherited, child in (
          ({flag: "true"}, SAFE_FLAGS),
          (SAFE_FLAGS, {flag: "true"}),
          ({}, {flag: "ambiguous"}),
      ):
        with self.subTest(flag=flag, inherited=inherited, child=child):
          await self.solve_for(
              {**NATIVE_ENV, **inherited}, relay_env=dict(child), rejected=True,
          )

  async def test_non_google_routes_preserve_cloud_flags_and_provider_priority(self):
    # Anthropic has priority even when the native Gemini base URL is present.
    routes = (
        (COMPATIBLE_ENV, "model"),
        ({**NATIVE_ENV, "ANTHROPIC_BASE_URL": "https://synthetic.invalid/anthropic"},
         "anthropic"),
    )
    for route, provider in routes:
      for flags in ({}, {"GOOGLE_GENAI_USE_ENTERPRISE": "true",
                         "GOOGLE_GENAI_USE_VERTEXAI": "ambiguous"}):
        with self.subTest(provider=provider, flags=flags):
          captured = await self.solve_for({**route, **flags}, relay_env=dict(flags))
          argv = captured["argv"]
          self.assertEqual(argv[argv.index("--provider") + 1], provider)
          self.assertEqual({flag: captured["env"][flag] for flag in SAFE_FLAGS
                            if flag in captured["env"]}, flags)


if __name__ == "__main__":
  unittest.main()
