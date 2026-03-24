# Changelog

The format is based on [Keep a Changelog](https://kSSeepachangelog.com/en/1.1.0/).

## [0.0.9] - 2026-03-24

### Added

- OpenAI wrapper (`jdlib.ai`) with async support and Django integration (`jdlib.django.ai`)
- `UUIDModelAdmin` to display `uuid`, `created_at`, and `updated_at` in admin
- Admin interface for `User` and `EmailUser`

### Removed

- Unused `jdlib.env` module

## [0.0.8] - 2026-03-23

### Added

- Mailgun backend (via `anymail`) with optional `django-rq` queuing

### Removed

- `jdlib.mail` and `jdlib.django.mail.send_mail` in favor of `jdlib.django.backends.EmailBackend`

### Security

- Fix command injection vulnerability in `jdlib secrets` commands

## [0.0.7] - 2026-03-20

### Added

- Manage secrets using `jdlib.secrets` module
- `ShellCommandMixin` for executing shell commands
- Call commands programatically using `call_command`

## [0.0.6] - 2026-03-20

### Added

- `jdcli` command line entry point with command routing

### Removed

- Remove overridden `User.email_user`

## [0.0.5] - 2026-03-05

### Added

- Django specific `send_mail` function. Used to surface unconfigured `settings.py` variables

### Changed

- Pass `domain` and `api_key` to `jdlib.mail.send_email` with environment fallback
- Swap `django.core.mail.send_mail` with `jdlib.django.mail.send_mail` for `User.email_user`

## [0.0.4] - 2026-03-05

### Added

- Parse environment variable using `env.get()`
- Send text emails using Mailgun

## [0.0.3] - 2026-03-03

### Added

- Environment parsing module `jdlib.env`

### Changed

- Moved `get_timezone_choices()` to `middleware.py`

## [0.0.2] - 2026-02-26

### Added

- `User`, `EmailUser`, `EmailUserManager`
- `TimezoneMixin` and `TimezoneMiddleware`

## [0.0.1] - 2026-02-26

### Added

- `AutoCreatedField`, `AutoUpdatedField`, `TimestampedMixin`
- `UUIDField`, `UUIDMixin`, `Model`

## [0.0.0] - 2026-02-26

### Added

- Library skeleton
