# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.12.0...HEAD

## [0.12.0][]

[0.12.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.11.0...0.12.0

### Changed

* Remove ujson to be more portable

## [0.11.0][]

[0.11.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.10.0...0.11.0

### Changed

* Send planning status back to Reliably
* Add span attributes and tags

## [0.10.0][]

[0.10.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.9.4...0.10.0

### Added

* Probe to measure duration of a single HTTP request
* Tolerance to validate this duration is below a certain value
* Probe to capture the TLS certificate of a remote endpoint
* Tolerances to validate aspects of the certificate

## [0.9.4][]

[0.9.4]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.9.3...0.9.4

### Added

* Added extra information to journal

## [0.9.3][]

[0.9.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.9.2...0.9.3

### Fixed

* Fix URL to execution

## [0.9.2][]

[0.9.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.9.1...0.9.2

### Changed

* Removing the execution payload from the extension

## [0.9.1][]

[0.9.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.9.0...0.9.1

### Fixed

* Ensure extension is stored

## [0.9.0][]

[0.9.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.8.1...0.9.0

### Changed

* Migrate to new Reliably API
* Add execution url and payload into the journal

## [0.8.1][]

[0.8.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.8.0...0.8.1

### Changed

* Always load settings from the config file first if it exists

## [0.8.0][]

[0.8.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.7.0...0.8.0

### Changed

* Always send the experiment encoded in standard base64

## [0.7.0][]

[0.7.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.6.0...0.7.0

### Changed

* Ensure events are properly referenced

## [0.6.0][]

[0.6.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.5.0...0.6.0

### Added

* Read `RELIABLY_TOKEN`, `RELIABLY_HOST` and `RELIABLY_ORG` environment
  variables when secrets have not been provided. They are common.
* Spec element to send to Reliably: contains the experiment and the output at various points in time

### Changed

* Major rework to match how Reliably's API currently works

## [0.4.2][]

[0.4.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.4.1...0.4.2

### Changed

* Very minor but fix link to image so documentation could get generated

## [0.4.1][]

[0.4.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.4.0...0.4.1

### Changed

* Fixed documentation regarding control usage

## [0.4.0][]

[0.4.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.3.0...0.4.0

### Changed

* Fixed labels sent to Reliably to use alias field names
* Corrected docstring examples of control usage
* Modified output label entry for experiment events to be strings
* Change `ctk_type` label entry to be `entity-type`
* Change url to reliably to now include `/api/*` as Reliably changed routes to
services

## [0.3.0][]

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.2.2...0.3.0

### Added

- Added `chaosreliably.controls`:
  - Added `before_experiment_control` to create an Experiment, Experiment Version,
    Experiment Run, and an Experiment Event (Start) within Reliably services.
  - Added `before_hypothesis_control` and `after_hypothesis_control` to create
    Experiment Events within Reliably services.
  - Added `before_method_control` and `after_method_control` to create Experiment
    Events within Reliably services.
  - Added `before_rollback_control` and `after_rollback_control` to create
    Experiment Events within Reliably services.
  - Added `before_activity_control` and `after_activity_control` to create
    Experiment Events within Reliably services.
  - Added `after_experiment_control` to create an Experiment Event within Reliably
    services

### Changed

- Updated `.github/workflows/build.yaml` to be in line with `chaostoolkit`
- Updated `Makefile` to be in line with `chaostoolkit`
- Add `check-pr.md` which alerts PR raisers to whether they've modified
`CHANGELOG.md` or tests.
- Ran `pyupgrade --py36-plus` on the project
- Bump up coverage in tests to cover failure cases in `__init__.py`
- Add `mypy` as a dependency and use it in linting to enforce typing

## [0.2.2][]

[0.2.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.2.1...0.2.2

- Updated `README.md` to correctly show where `tolerance` goes when using `slo_is_met` as a Steady State Hypothesis
- Fixed default reliably host to be `reliably.com` instead of `api.reliably.com`

## [0.2.1][]

[0.2.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.2.0...0.2.1

### Changed

- Updated `get_objective_results_by_labels` to have a default `limit` of `1`
- Add `slo_is_met` as a probe to encompass the `get_objective_results_by_labels` probe and `all_objective_results_ok` tolerance


## [0.2.0][]

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.1.2...0.2.0

### Changed

- Fix issue where secrets were not correctly extracted from Experiment config [#1][1]
- Refactor to use new Reliably Entity Server rather than previous API
  - One probe available: `get_objective_results_by_labels`
    - For a given Objectives labels, get the Objective Results
  - One tolerance available: `all_objective_results_ok`
    - For a list of Objective Results, determine if they were all OK
- Allow for user to provide `org` as a secret/get it from `currentOrg` in their Reliably config

[1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/issues/1

## [0.1.2][]

[0.1.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.1.1...0.1.2

### Changed

- Use the most recent SLO report only

## [0.1.1][]

[0.1.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/compare/0.1.0...0.1.1

### Changed

- Add `install_requires` so that dependencies are properly installed via pip

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-reliably/tree/0.1.0

### Added

-   Initial release
