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
from collections.abc import Sequence
from datetime import date, datetime

import pytz
from mkdocs.config import config_options as c
from mkdocs.config.base import Config as BaseConfig
from mkdocs.plugins import BasePlugin
from pytz import timezone

logger = logging.getLogger("mkdocs.plugins." + __name__)
TAG = "[calendar] -"


class CalendarPluginConfig(BaseConfig):
    """Configuration options for the calendar plugin."""

    start = c.Optional(c.Type(date))
    end = c.Optional(c.Type(date))
    tz = c.Choice(pytz.all_timezones, default="UTC")
    week_names = c.Type(list, default=[])
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
        week_names = self.get_xconfig(config, "week_names") or []
        cal = {
            "now": now,
            "today": now.date(),
            "weekday": now.weekday(),
            "week_number": now.isocalendar()[1],
            "iso_weekday": now.isoweekday(),
        }

        if start_date is not None:
            # pylint: disable-next=invalid-name
            aw = ((now.date() - start_date).days) // 7
            cal["academic_week"] = aw + 1
            if isinstance(week_names, Sequence) and 0 <= aw < len(week_names):
                cal["academic_week_name"] = week_names[aw]
            else:
                cal["academic_week_name"] = None

            cal["start"] = start_date
            cal["elapsed"] = (now.date() - start_date).days
            cal["elapsed_weeks"] = cal["elapsed"] / 7

            cal["aw"] = cal["academic_week"]
            cal["awn"] = cal["academic_week_name"]

        if end_date is not None:
            cal["end"] = end_date
            cal["remaining"] = (end_date - now.date()).days
            cal["remaining_weeks"] = cal["remaining"] / 7

        config.extra[self.config["extra_key"]] = cal

        return config
