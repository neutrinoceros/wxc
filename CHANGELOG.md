# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to

## [6.6.0] - 2022-07-20

BUG: fix a bug where version look up table's order wasn't being preserved
[PR #152](https://github.com/neutrinoceros/wxc/pull/152)

ENH: implement fast lookups for simple queries (module location and version)
[PR #161](https://github.com/neutrinoceros/wxc/pull/161)

## [6.5.5] - 2021-11-15

MNT: bump required rich version to 10.13, adapt tests accordingly (no actual change in behaviour)
[PR #144](https://github.com/neutrinoceros/wxc/pull/144)

## [6.5.4] - 2021-11-15

BUG: fix a crash when calling `wxc <pkg> --full` for packages for which no implemented method
to get the version tag works.
[PR #142](https://github.com/neutrinoceros/wxc/pull/142)


## [6.5.3] - 2021-09-04

ENH: add fallback support for properties, which are not yet supported by inspect.getfile
[PR #136](https://github.com/neutrinoceros/wxc/pull/136)

## [6.5.2] - 2021-09-03

ENH: disable source line printing by default, add a flag to reactivate them [PR
#133](https://github.com/neutrinoceros/wxc/pull/133)

## [6.5.1] - 2021-08-26

BUG: fix an issue where failing calls to inspect.getsource would leak as Python errors

## [6.5.0] - 2021-08-25

- ENH: add rich transient progress spinner [PR #124](https://github.com/neutrinoceros/wxc/pull/124)
- EHN: add --source argument (use rich to display source code) [PR #125](https://github.com/neutrinoceros/wxc/pull/125)
- ENH: add rich colors to error messages [PR #129](https://github.com/neutrinoceros/wxc/pull/129)

## [6.4.0] - 2021-08-25

- ENH: improve error message in case package name is falty
- ENH: normalize module names in a similar fashion to pip (replace hyphens '-' with underscores '_' at runtime)

This release contains a breaking change for any user relying on the public
Python API (`wxc.api`) because the signature of `wxc.api.get_suggestions` was changed.

## [6.3.2] - 2021-08-23

FIX: fix a important distinction between builtin functions and C-compiled functions
     in an error message.

## [6.3.1] - 2021-08-22

ENH: deactivate (rich) colored output for version numbers

## [6.3.0] - 2021-08-19

- ENH: improve type checking with mypy
- FEAT: support colored printing if rich is installed (optional dependency)

## [6.2.10] - 2021-08-16

- ENH: improve internal string formatting, fix a broken fstring
- FIX: fix a typo in module name (levenshtein.py -> levenshtein.py)
- ENH: improve suggestions in case of typo (always show the closest match)

## [6.2.9] - 2021-08-16

UX: improve error message in case of missing attribute

## [6.2.8] - 2021-08-10

FIX: fix a bug where calling `wxc wxc.__main__` would run the main function twice.

## [6.2.7] - 2021-07-04

MAINT: add Windows to officially supported platforms.
This version is identical to 6.2.6, only testing infrastructure was updated.

## [6.2.6] - 2021-07-04

Hotfix a bug introduced in version 6.2.5, further improvements for queries on
builtin objects.

## [6.2.5] - 2021-07-03

UX: improvements in support to queries on builtin objects.

## [6.2.4] - 2021-06-30

Improve version checking support for some builtin packages (e.g. `tarfile`) that with a
lowercase `'version'` attribute.

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
