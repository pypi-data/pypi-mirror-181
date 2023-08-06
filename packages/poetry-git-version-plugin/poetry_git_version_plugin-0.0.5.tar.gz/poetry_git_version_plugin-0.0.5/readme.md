# Poetry Git Version Plugin

Poetry plugin to get package version from git.

> Descendant of `poetry-version-plugin`, which **does not work** on `poetry 1.2.0`.

## Functionality

- Project tag parsing
- Substitution of the project tag (if any) in the poetry.version value
- Maintenance of PEP 440
- Command to output a new version

## Quick start

```bash
poetry self add poetry-git-version-plugin
poetry git-version # Write your git tag
poetry -v git-version # print process
```

## Dependencies

```toml
[tool.poetry.dependencies]
python = ">=3.10"
poetry = ">=1.2.0"
```

## Setup

```toml
[tool.poetry-git-version-plugin]
# Ignore "tag missing" errors
ignore_exception = true

# If the tag is missing.
# Returns a version, computed from the latest version tag.
# It takes the version tag, increases the version tag by the number of commits since, adds a local label specifying the git commit hash and the dirty status.
# Example: 1.3.2+5-5babef6
use_last_tag = true
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/poetry-git-version-plugin>
