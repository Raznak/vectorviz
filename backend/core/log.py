from core.settings import settings
from datetime import datetime
from logging import Formatter
import logging
import json


class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record):
        json_record = {
            "date": datetime.utcnow().isoformat(),
            "level": settings.LOG_LEVEL,
        }
        json_record["message"] = record.getMessage()

        if record.exc_info:
            json_record["exc_info"] = record.exc_info

        return json.dumps(json_record)


logger = logging.root
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(settings.LOG_LEVEL)
