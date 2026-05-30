# SciPlex Configuration

This directory holds skill-level default configuration. A research workspace can
override these values by creating its own `sciplex/config/` directory.

## Precedence

SciPlex resolves configuration from highest priority to lowest priority:

1. Project private env: `<workspace>/sciplex/config/.env.local`
2. Project non-secret config: `<workspace>/sciplex/config/config.yaml`
3. Skill private env: `<skills>/sciplex/config/.env.local`
4. Skill non-secret config: `<skills>/sciplex/config/config.yaml`
5. Driver agent environment
6. Built-in safe defaults

Project-level config is for one research project. Skill-level config is for
reusable user or machine defaults. Driver-level fallback is only a last resort.

## Driver vs Internal LLM

The agent that starts SciPlex is the driver agent. It may be Claude, Codex, a
local CLI, or another orchestrator. SciPlex internal LLM settings are separate
from the driver agent.

If project and skill config do not specify an internal LLM provider, SciPlex may
inherit the driver agent's current LLM environment. This fallback should be
explicitly recorded in the resolved config snapshot.

Use task-specific profiles when useful:

```env
SCIPLEX_LLM_DEFAULT=<model-name>
SCIPLEX_LLM_LITERATURE=<model-name>
SCIPLEX_LLM_METHOD=<model-name>
SCIPLEX_LLM_REVIEW=<model-name>
SCIPLEX_LLM_WRITING=<model-name>
```

## Literature Providers

Literature provider configuration is independent from LLM configuration.

- OpenAlex can usually run without an API key; provide an email when possible.
- arXiv can usually run without an API key.
- Zotero requires `ZOTERO_USER_ID` and `ZOTERO_API_KEY`.
- Semantic Scholar may work without a key at lower limits, but a key is more
  reliable.
- Private or proprietary providers must be disabled when credentials are absent.

Missing credentials should degrade the provider list, not break unrelated
workflow phases.

## Workspace Config

On initialization, create:

```text
sciplex/
  config/
    .env.local
    config.yaml
    resolved.json
```

`config.yaml` is for non-secret project settings. `.env.local` is for private
project overrides and should not be committed. `resolved.json` is optional and
should contain only redacted values plus provider/model status for audit.

## Secret Handling

Never write raw API keys or tokens into:

- `state.json`
- `events.json`
- `objects/`
- `objects/console/console_data.json`
- manuscripts or reports
- `config/resolved.json`

Resolved config snapshots should record values as `<set>`, `<unset>`,
`<redacted>`, or provider-specific status such as `enabled`, `disabled`, or
`degraded`.
