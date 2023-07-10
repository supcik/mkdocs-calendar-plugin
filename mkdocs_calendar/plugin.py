################################################################################
# @brief       : Calendar plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 17. June 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2023 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT OR Apache-2.0
################################################################################

"""Calendar plugin for MkDocs"""

import logging
import time
from datetime import date, datetime

import pytz
from mkdocs.config import config_options as c
from mkdocs.config.base import Config as BaseConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from pytz import timezone

logger = logging.getLogger("mkdocs.plugins." + __name__)
TAG = "[calendar] -"


class CalendarPluginConfig(BaseConfig):
    """Configuration options for the calendar plugin."""

    start = c.Optional(c.Type(date))
    end = c.Optional(c.Type(date))
    tz = c.Choice(pytz.all_timezones, default="Europe/Zurich")
    weeks_off = c.Type(list, default=[])
    extra_key = c.Type(str, default="cal")


# pylint: disable-next=too-few-public-methods
class CalendarPlugin(BasePlugin[CalendarPluginConfig]):
    """Calendar plugin for MkDocs"""

    def get_xconfig(self, config, key):
        """Get the configuration value for the given key."""
        if "calendar_plugin" in config.extra:
            extra = config.extra["calendar_plugin"]
            if key in extra:
                return extra[key]
        if key in self.config:
            return self.config[key]
        return None

    def on_config(self, config):
        """Validate the configuration and add calendar entries to the config."""
        now = datetime.fromtimestamp(time.time(), tz=timezone(self.config["tz"]))

        start_date = self.get_xconfig(config, "start")
        end_date = self.get_xconfig(config, "end")
        weeks_off = self.get_xconfig(config, "weeks_off") or []
        cal = {
            "now": now,
            "today": now.date(),
            "weekday": now.weekday(),
            "week_number": now.isocalendar()[1],
            "iso_weekday": now.isoweekday(),
        }

        if start_date is not None:
            academic_week = ((now.date() - start_date).days) // 7 + 1
            try:
                for i in weeks_off:
                    if academic_week >= i:
                        academic_week -= 1
            except Exception as e:  # pylint: disable=invalid-name
                raise PluginError(f"{TAG} : {e}") from e

            cal["start"] = start_date
            cal["delta"] = (now.date() - start_date).days
            cal["delta_w"] = ((now.date() - start_date).days) / 7
            cal["academic_week"] = academic_week
            cal["aw"] = academic_week

        if end_date is not None:
            cal["end"] = end_date
            cal["remaining"] = (end_date - now.date()).days

        config.extra[self.config["extra_key"]] = cal

        return config
