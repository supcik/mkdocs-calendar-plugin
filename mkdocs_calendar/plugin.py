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

import collections.abc
import logging
import time
from datetime import date, datetime

import jinja2
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
    weeks_off = c.Type(list, default=[])
    config_keys_to_fix = c.Type(list, default=[])
    extra_key = c.Type(str, default="cal")


# pylint: disable-next=too-few-public-methods
class CalendarPlugin(BasePlugin[CalendarPluginConfig]):
    """Calendar plugin for MkDocs"""

    def _fix_item(self, key, config, jinja_env):
        subconfig = config
        path = key.split(".")
        for stem in path[:-1]:
            if stem not in subconfig:
                logger.warning("%s Key '%s' not found in config... skipping", TAG, key)
                return
            if not isinstance(subconfig[stem], collections.abc.Mapping):
                logger.warning(
                    "%s - Invalid key '{%s}' [%s]... skipping",
                    TAG,
                    key,
                    type(subconfig[stem]),
                )
                return
            subconfig = subconfig[stem]

        if path[-1] not in subconfig:
            logger.warning("%s - Key '{%s}' not found in config... skipping", TAG, key)
            return

        orig = subconfig[path[-1]]
        template = jinja_env.from_string(orig)

        try:
            subconfig[path[-1]] = template.render(today=self.today)
        except jinja2.TemplateError as e:  # pylint: disable=invalid-name
            logger.warning("%s - Failed to render '%s': %s", TAG, key, e)
            subconfig[path[-1]] = orig

    def on_config(self, config):
        """Validate the configuration and add calendar entries to the config."""
        now = datetime.fromtimestamp(time.time(), tz=timezone(self.config["tz"]))

        start_date = self.config["start"]
        end_date = self.config["end"]

        academic_week = ((now.date() - start_date).days) // 7 + 1
        try:
            for i in self.config["weeks_off"]:
                if academic_week >= i:
                    academic_week -= 1

        except Exception as e:  # pylint: disable=invalid-name
            raise PluginError(f"{TAG} : {e}") from e

        cal = {
            "start": start_date,
            "end": end_date,
            "now": now,
            "today": now.date(),
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

        env = jinja2.Environment()
        for key in self.config.config_keys_to_fix:
            self._fix_item(key, config, env)

        return config
