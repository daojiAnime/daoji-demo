# CLAUDE.md

Response always use 中文.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Repository overview
- Python 3.12 project managed with uv (see .cursor/rules/python-packages-manager.mdc:11-16). Packaging via hatchling (pyproject.toml:90-92).
- Main library package: daoji_demo (daoji_demo/__init__.py, daoji_demo/traffic.py). CLI entry point aws-traffic (pyproject.toml:39-41) maps to daoji_demo.traffic:main (daoji_demo/traffic.py:234-244).
- Tests: pytest with config in pytest.ini. Test files under tests/ and top-level test_llm_reason.py.
- Tooling: ruff configured in pyproject for lint/format, mypy strict mode in pyproject, additional mypy.ini present for legacy paths, pyright minimal config, Dockerfile unrelated to this repo layout (uses poetry/app). Cursor rules included; important: use uv for Python package management, and follow FastAPI style if touching web code.

Common commands
- Install deps: uv sync
- Add dev deps: uv add --group dev <pkg>
- Run tests: uv run pytest
- Run a single test file: uv run pytest -q tests/test_logger.py
- Run a single test by name: uv run pytest -k <name>
- Verbose live logs per pytest.ini: uv run pytest -vv -s
- Lint: uv run ruff check .
- Lint and fix: uv run ruff check --fix . or scripts/format.sh
- Type check (mypy, strict set in pyproject): uv run mypy .

Project architecture
- daoji_demo/traffic.py: Typer CLI for AWS Lightsail bandwidth reporting using boto3. Uses dotenv to load credentials (.env.example shows keys). Entry function main() invokes Typer app run command that aggregates instance NetworkIn/Out and optionally stops instances over 95% quota. Key helpers: get_current_month_first_day_zero_time(), get_current_month_last_day_last_time(), list_instances(), get_month_dto_quota(), get_instance_data_usage(), get_percent_color(), run() (Typer command), main().
- tests/: pytest config and simple logger test; test_llm_reason.py includes async OpenAI/OpenRouter streaming examples and assertions around model outputs. Note it references modules like configs and logics.* that are not present; treat it as experimental code, not core library tests.
- Tooling config: pyproject.toml defines dependencies, ruff, mypy, pyright, and uv settings; pytest.ini sets warnings as errors and live logging; mypy.ini appears to target paths not present here—prefer tool.mypy config in pyproject.toml.
- Cursor rules: prefer uv for package execution and management; if working on FastAPI components (not currently in this package), follow fastapi.mdc conventions.

Environment and secrets
- Use python-dotenv; create a local .env from .env.example with AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION for aws-traffic.
- Do not commit real credentials.

Running the CLI
- aws-traffic (installed via uv tool or uv run): uv run aws-traffic run
- Disable auto-stop behavior: uv run aws-traffic run --no-auto-stop

Notes for future changes
- Maintain Typer CLI patterns and rich output style used in daoji_demo/traffic.py.
- Keep ruff and mypy happy; line length 120, target Python 3.12.
- Prefer uv run to execute tools and tests. Avoid adding Poetry-specific scripts unless the project migrates.
