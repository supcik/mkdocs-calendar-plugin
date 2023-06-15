################################################################################
# @brief       : Calendar plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 14. June 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2022 HEIA-FR / ISC
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

    start = c.Type(date)
    end = c.Type(date)
    tz = c.Choice(pytz.all_timezones, default="Europe/Zurich")
    academic_weeks_off = c.Type(list, default=[])


# pylint: disable-next=too-few-public-methods
class CalendarPlugin(BasePlugin[CalendarPluginConfig]):
    """Calendar plugin for MkDocs"""

    def on_config(self, config):
        """Validate the configuration and add calendar entries to the config."""
        now = datetime.fromtimestamp(time.time(), tz=timezone(self.config["tz"]))

        start_date = self.config["start"]
        end_date = self.config["end"]

        academic_week = ((now.date() - start_date).days) // 7 + 1
        try:
            for i in self.config["academic_weeks_off"]:
                if academic_week >= i:
                    academic_week -= 1

        except Exception as e:  # pylint: disable=invalid-name
            raise PluginError(f"{TAG} : {e}") from e

        cal = {
            "start": start_date,
            "end": end_date,
            "now": now,
            "weekday": now.weekday(),
            "week_number": now.isocalendar()[1],
            "iso_weekday": now.isoweekday(),
            "today": now.date(),
            "delta": (now.date() - start_date).days,
            "delta_w": ((now.date() - start_date).days) / 7,
            "academic_week": academic_week,
            "aw": academic_week,
            "remaining": (end_date - now.date()).days,
        }

        config.extra["cal"] = cal

        return config
