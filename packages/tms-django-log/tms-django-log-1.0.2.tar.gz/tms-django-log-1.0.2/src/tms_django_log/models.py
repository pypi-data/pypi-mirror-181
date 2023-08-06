import logging
import traceback
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _

logger = logging.getLogger(__name__)


class LogLevel(models.TextChoices):
    TRACE = "0", _("Trace")
    DEBUG = "1", _("Debug")
    INFO = "2", _("Info")
    WARNING = "3", _("Warning")
    CRITICAL = "4", _("Critical")
    FATAL = "5", _("Fatal")


class Log(models.Model):
    message = models.CharField(max_length=512, primary_key=True)
    level = models.CharField(max_length=2, default="0", choices=LogLevel.choices)
    detail = models.TextField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    traceback = models.TextField(null=True, blank=True)


def add_log(message, detail=None, level=1):
    log, created = Log.objects.get_or_create(message=message)
    log.count += 1
    log.traceback = traceback.format_exc()
    log.detail = detail
    log.level = level
    log.save()
    if int(level) == 1:
        logger.debug(f"{message}")
    elif int(level) == 2:
        logger.info(f"{message}")
    elif int(level) == 3:
        logger.warning(f"{message}")
    elif int(level) > 3:
        logger.error(f"{message}")
    else:
        logger.debug(f"{message}")
