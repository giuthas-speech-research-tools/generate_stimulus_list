# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[//]: # (Possible headings in a release:)
[//]: # (Highlights for shiny new features.)
[//]: # (Added for new features.)
[//]: # (Changed for changes in existing functionality.)
[//]: # (Refactor when functionality does not change but moves.)
[//]: # (Documentation for updates to docs.)
[//]: # (Testing for updates to tests.)
[//]: # (Deprecated for soon-to-be removed features.)
[//]: # (Removed for now removed features.)
[//]: # (Fixed for any bug fixes.)
[//]: # (Security in case of vulnerabilities.)
[//]: # (New contributors for first contributions.)

[//]: # (And ofcourse if a version needs to be YANKED:)
[//]: # (## [version number] [data] [YANKED])


## [Unreleased]

### Roadmap to 2.0
- [ ] Main code modernization:
  - [x] Start using branches in git
  - [x] Come up with a better package name and check that it is available on PyPi
  - [x] Move the code to source directory
  - [ ] Get a package management tool
    - [ ] Create environments for at least: stable version, development, testing
    - [ ] Proper python packaging for installation
    - [ ] Provide an entry point for running as a generic commandline tool
    - [ ] Upload on PyPi
  - [ ] Implement the cli in click
  - [ ] Documentation
	  - [ ] generate API
	  - [ ] write usage samples etc
	  - [ ] see that the CLI helps work as they should
  - [ ] Start using license headers  
  
### Roadmap after 2.0
- [ ] Add a batch run options file so that settings can be saved and
  replicated.
- [ ] Make beep generation optional
- [ ] Make randomisation optional
- [ ] Add option of using end_calibration as an input file
- [ ] Write exporter to RASL format
- [ ] Provide examples

Possibly also:

- [ ] testing, which might rely on the examples

## [1.0.2] 2024-11-11

### Changed
- Package name is now the simpler Generate Stimulus List.
- Updated Roadmap above

### Added

- This Changelog.