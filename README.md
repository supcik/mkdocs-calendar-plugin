# mkdocs-calendar-plugin

This MkDocs plugin exposes calendar information to the 'extra' configuration variable.
This plugin is particularly useful when used together with the
[mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

## Installation

Install the package with pip:

```bash
pip install mkdocs-calendar-plugin
```

Activate the plugin in `mkdocs.yml`:

```yaml
plugins:
  - search
  - calendar
  - macros
```

## Configuration

The plugin can be configured in the `plugins` section of `mkdocs.yml` as follows:

```yaml
plugins:
  - search
  - calendar:
      tz: Europe/Zurich
      start: 2023-02-20
      end: 2023-06-23
  - macros
```

It can be more convenient to use the `extra` configuration variable, so that the `plugin` section of `mkdocs.yml` can be kept clean.
`mkdocs-calendar-plugin` can also be configured using the `extra.calendar_plugin` configuration variable as follows:

```yaml
extra:
  calendar_plugin:
    start: 2023-02-20
    end: 2023-06-23

plugins:
  - search
  - calendar:
      tz: Europe/Zurich
  - macros
```

The plugin supports the following configuration options:

| Option       | Description                                                              |
|--------------|--------------------------------------------------------------------------|
| `tz`         | The timezone to use for the calendar. Defaults to `UTC`.                 |
| `start`      | The start date of the calendar.                                          |
| `end`        | The end date of the calendar.                                            |
| `week_names` | The names of the weeks. Defaults to `[]` (no week names).                |
| `extra_key`  | The key to use in the `extra` configuration variable. Defaults to `cal`. |

## Extra configuration variable

The plugin exposes the following information in the `extra.<extra_key>` configuration variable:

| Key                  | Description                                                                                                                                    |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `now`                | The current date and time                                                                                                                      |
| `today`              | The current date                                                                                                                               |
| `weekday`            | The current weekday (Monday == 0 ... Sunday == 6)                                                                                              |
| `iso_weekday`        | The current ISO weekday (Monday == 0 ... Sunday == 7)                                                                                          |
| `week_number`        | The current ISO week number                                                                                                                    |
| `start`              | A copy of `extra.<extra_key>.start` _(only if `extra.<extra_key>.start` is defined)_                                                           |
| `academic_week`      | The academic week number staring from `extra.<extra_key>.start` _(only if `extra.<extra_key>.start` is defined)_                               |
| `academic_week_name` | The academic week name (from the `week_names` array) staring from `extra.<extra_key>.start` _(only if `extra.<extra_key>.start` is defined)_-- |
| `elapsed`            | The number of days elapsed since `extra.<extra_key>.start` _(only if `extra.<extra_key>.start` is defined)_                                    |
| `elapsed_weeks`      | The number of weeks elapsed since `extra.<extra_key>.start` _(only if `extra.<extra_key>.start` is defined)_                                   |
| `aw`                 | alias for `academic_week`  _(only if `extra.<extra_key>.start` is defined)_                                                                    |
| `awn`                | alias for `academic_week_name`    _(only if `extra.<extra_key>.start` is defined)_                                                             |
| `end`                | A copy of `extra.<extra_key>.end` _(only if `extra.<extra_key>.end` is defined)_                                                               |
| `remaining`          | The remaining days to `extra.<extra_key>.end` _(only if `extra.<extra_key>.end` is defined)_                                                   |
| `remaining_weeks`    | The remaining weeks to `extra.<extra_key>.end` _(only if `extra.<extra_key>.end` is defined)_                                                  |
