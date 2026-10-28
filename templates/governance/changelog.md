<!--
Copy to CHANGELOG.md at the package root. Format: Keep a Changelog 1.1.0 with design-system
sections (beyond the book). Versions follow semver. Replace <prefix>, <version>, <date>, <repo>.
Delete the example lines in the first release.
-->

# Changelog

All notable changes to <prefix> are recorded here. Each entry names the pattern or token, links
the pull request, and marks breaking changes with **BREAKING**.

## [Unreleased]

### Added patterns
### Changed
### Deprecated
### Removed
### Fixed
### Tokens

## [<version>] - <YYYY-MM-DD>

### Added patterns
- `<pattern>`: <one line> (Beta). [#<pr>](<repo>/pull/<pr>)

### Changed
- `<pattern>`: <what changed and what to retest; paste its "used in" list>. [#<pr>](<repo>/pull/<pr>)

### Deprecated
- `<pattern-or-token>`: use `<replacement>` instead. Earliest removal: <major-version>.
  Notice: `design-system/docs/deprecations/<name>.md`

### Removed
- **BREAKING** `<pattern-or-token>`: deprecated in <version>. Migration: <link>.

### Fixed
- `<pattern>`: <bug>. [#<pr>](<repo>/pull/<pr>)

### Tokens
- Added: `<token.path>`
- Changed: `<token.path>` <old value> → <new value> (brands affected: <brands>)
- Deprecated: `<token.path>` → `<replacement.path>`
- Removed: **BREAKING** `<token.path>`

[Unreleased]: <repo>/compare/v<version>...HEAD
[<version>]: <repo>/releases/tag/v<version>
