# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [6.2.3] - 2021-06-18

Update documentation to reflect Python 3.10 support.

## [6.2.2] - 2021-06-10

Improve dependency specifications: stop requiring `importlib_metadata` for
Python versions newer than 3.7

## [6.2.1] - 2021-06-05
Fix a streaming error, properly direct error message to stderr.

## [6.2.0] - 2021-06-04
Added provisional support for Python 3.10 (tested with 3.10.0-beta2)

## [6.1.2] - 2021-05-10
### Added
- maint: fix a typo in a filename

## [6.1.1] - 2021-05-10
### Added
- maint: drop dependency to numpy for typo correction suggestions.

## [6.1.0] - 2021-05-10
### Added
- UX: better error messages in case of typos, suggest possible corrections.

## [6.0.0] - 2021-04-25
Renamed the project from pyw to wxc, first publication on Pypi.
