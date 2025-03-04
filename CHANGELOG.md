# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.12.2] - 2025-03-04

### Changed

- Removed dummy `/api/status` endpoint, and disabled Uvicorn Access Log. Related to #13

## [0.12.1] - 2025-03-04

### Fixed

- Added a dummy `/api/status` endpoint, which always returns a successful response. #17, fixes #13

## [0.12.0] - 2025-02-20

### Added

- Add MkDocs documentation for the Dronetag Agent (#5)

### Changed

- In case of unknown speed accuracy, the track direction patch logic will assume 20 m/s uncertainty
- Setup docs are only available to people with an @starcopter.com email address (#10)

### Fixed

- Fixed OPRN input field to always smoothly connect with the button (#6)

## [0.11.0] - 2025-02-13

### Added

- Added velocity threshold to ground course broadcast (#4)

### Changed

- HTML templates are now rendered with Jinja2 Fragments (#3)

## [0.10.1] - 2025-01-24

### Removed

- Removed unused Bootstrap Javascript dependency

## [0.10.0] - 2025-01-23

### Added

- Limit accepted ISO 3166-1 Alpha-3 country codes to EU member states (#2)
- Build and release application with GitHub Actions (#1)

## [0.9.0] - 2024-03-19

### Added

- Initial release of the Dronetag Agent
- MAVLink relay to couple a Dronetag DRI module with Skynode
- Web UI for configuration and monitoring
- Support for UAS Operator Registration Number (OPRN)
- Integration with Auterion OS as an Auterion App
- FastAPI-based web service
- MAVLink message handling for drone identification
- Configuration management via web interface
- Documentation for installation and usage

[unreleased]: https://github.com/starcopter/dronetag-agent/compare/v0.12.2...HEAD
[0.12.2]: https://github.com/starcopter/dronetag-agent/compare/v0.12.1...v0.12.2
[0.12.1]: https://github.com/starcopter/dronetag-agent/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/starcopter/dronetag-agent/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/starcopter/dronetag-agent/compare/v0.10.1...v0.11.0
[0.10.1]: https://github.com/starcopter/dronetag-agent/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/starcopter/dronetag-agent/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/starcopter/dronetag-agent/compare/616ebe24fbfd3e404e157928bfe7af73369001e3...v0.9.0
