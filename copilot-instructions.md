## Copilot / Repository Instructions — Python Best Practices

Purpose
-------
This document describes recommended best practices for Python projects. It's intended as a concise checklist and guidance for new contributors and automated assistants (like Copilot) to follow when creating or modifying Python code in this repository.

Quick contract
--------------
- Inputs: Python source files and configuration in the repository.
- Outputs: Well-structured, test-covered, type-checked, linted, and formatted code ready for CI and release.
- Error modes: Missing/incorrect dependencies, failing tests, style/typing errors.
- Success: Code passes tests, linters, and CI; new features include tests and docs; packaging artifacts build successfully.

Repository layout (recommended)
------------------------------
Use a simple, conventional layout:

```
repo-root/
  README.md
  pyproject.toml  # preferred for modern projects
  setup.cfg or setup.py  # if packaging legacy
  requirements.txt  # optional, for simple setups or pinned deploys
  src/  # or package-name/
    package_name/
      __init__.py
      module.py
  tests/
  docs/  # optional
  .gitignore
  .pre-commit-config.yaml
```

Why `src/` layout? It avoids import-on-test-time issues and clearly separates source from other files.

Tooling & dependency management
------------------------------
- Use `pyproject.toml` for build-system configuration (PEP 518). Tools: Poetry, Flit, or setuptools with config in `pyproject.toml`.
- For environments use `venv`/virtualenv, or Poetry/Conda if the project needs it. Always document how to create the environment in `README.md`.
- Pin direct dependencies for reproducible builds (use a lock file: `poetry.lock`, `pip-tools` generated `requirements.txt`, or `pipenv`).

Formatting, linting & style
-------------------------
- Formatting: use Black. Configure line-length (88 or 100) in `pyproject.toml` if needed.
- Imports: use isort and integrate it with Black. Add an isort profile in `pyproject.toml`.
- Linting: run flake8 or ruff for fast linting. Keep rules minimal and actionable.
- Encourage type hints: run mypy (or ruff/mypy combo). Consider gradual typing with `# type: ignore` sparingly.

Testing
-------
- Use pytest for unit and integration tests.
- Keep tests in a top-level `tests/` directory mirroring package structure.
- Test types:
  - Unit tests: fast, isolated.
  - Integration tests: external resources mocked or run in CI with service containers.
- Use coverage (coverage.py or pytest-cov). Aim for meaningful coverage not arbitrary numbers; cover critical logic and edge cases.

Continuous Integration (CI)
--------------------------
- Run tests, linters, type-checks, and security checks on PRs.
- Typical CI steps:
  1. Create Python environment (matrix for different versions if supported).
  2. Install dependencies from lockfile.
 3. Run linters and formatters (format only locally; CI should check for diffs).
 4. Run mypy and/or static analysis.
 5. Run pytest with coverage.

Security and secrets
--------------------
- Never commit secrets or credentials. Use environment variables or a secrets manager.
- Add common secret patterns to `.gitignore` and use pre-commit secret hooks to detect accidental commits.

Configuration management
------------------------
- Keep configuration (non-secret) in files like `config.yaml`, `pyproject.toml`, or `env.example`.
- Prefer 12-factor principles: environment for runtime config, not source.

Packaging & releases
--------------------
- Prefer building wheels and sdist from `pyproject.toml` using `build` or `poetry build`.
- Use semantic versioning for releases (MAJOR.MINOR.PATCH).
- Tag releases in git and attach signed artifacts in release pipelines where possible.

Pre-commit and developer experience
----------------------------------
- Install `pre-commit` hooks to run Black, isort, and basic linters before commits.
- Provide setup scripts in `README.md` to create venv, install dev requirements, and enable pre-commit hooks.

Logging, errors and observability
--------------------------------
- Use the standard `logging` module; structure logs clearly with context and levels.
- Handle exceptions explicitly; avoid broad excepts. Fail fast when encountering unrecoverable states.

Performance and async
---------------------
- Profile before optimizing. Use `timeit`, `cProfile`, or benchmark suites.
- Prefer async (asyncio) for I/O-bound concurrency; document concurrency choices and limits.

Code review and PR guidance
--------------------------
- Small, focused PRs.
- Include tests and update docs when behavior changes.
- Reference related issues and the changelog entry for non-trivial changes.

Minimal pre-commit config suggestions
-----------------------------------
- Black
- isort
- ruff or flake8
- detect-secrets (or git-secrets)

Example quick checklist for PRs
------------------------------
1. Code has unit tests for new logic.
2. Code is formatted with Black; isort applied.
3. Linters (ruff/flake8) pass locally.
4. mypy (or type checks) pass for changed modules.
5. No secrets or large files were added.
6. README/docs updated if public API or behavior changed.

Helpful commands
----------------
Use these locally to follow the guidelines:

```
# create venv and install
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-dev.txt

# run formatters and linters
black .
isort .
ruff check .

# run tests with coverage
pytest --cov=package_name tests/

# run mypy
mypy src/package_name
```

Further reading
---------------
- PEP 8 — Style Guide for Python Code
- PEP 518 — pyproject.toml
- Packaging tutorials (Python Packaging User Guide)

Notes for automated assistants
-----------------------------
- When suggesting code changes, prefer minimal diffs, keep style consistent with repository, and add or update tests for behavior changes.
- If adding dependencies, prefer stable, well-maintained libraries and update lock files accordingly. Mention the reason in the PR body.

Contact / Contributing
----------------------
If you want to change these guidelines, open a PR describing the motivation and example changes. Keep the guidance pragmatic and focused on improving code quality and contributor experience.

-- End of file
