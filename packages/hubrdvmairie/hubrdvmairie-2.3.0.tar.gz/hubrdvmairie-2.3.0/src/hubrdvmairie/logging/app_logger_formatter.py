import json
import logging
import re
from datetime import datetime, timezone


def get_app_log(record):
    json_obj = {
        "log.level": record.levelname,
        "type": "app",
        "@timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "message": record.message,
    }

    if hasattr(record, "extra_info"):
        for key in record.extra_info:
            json_obj[key] = record.extra_info[key]

    return json_obj


def get_access_log(record):
    json_obj = {
        "log.level": record.levelname,
        "type": "access",
        "@timestamp1": datetime.strptime(
            record.asctime, "%Y-%m-%d %H:%M:%S,%f"
        ).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        + "Z",
        "@timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "message": record.message,
        "response_time": record.extra_info["response_time"],
        "protocol": record.extra_info["protocol"],
    }
    for key in record.extra_info:
        json_obj[key] = record.extra_info[key]
    return json_obj


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_valide_user_data(record):
    if "searchCriteria" not in record.extra_info:
        return True
    searchCriteria = record.extra_info["searchCriteria"]
    try:
        valide = (
            searchCriteria["radius_km"] in ["20", "40", "60"]
            and bool(datetime.strptime(searchCriteria["start_date"], "%Y-%m-%d"))
            and bool(datetime.strptime(searchCriteria["end_date"], "%Y-%m-%d"))
            and isfloat(searchCriteria["longitude"])
            and isfloat(searchCriteria["latitude"])
            and bool(
                re.match(r"^[A-zÀ-ú',-.\s]{1,70}[0-9]{5}$", searchCriteria["address"])
            )
        )
    except ValueError:
        valide = False
    return valide


class CustomFormatter(logging.Formatter):
    def __init__(self, formatter):
        logging.Formatter.__init__(self, formatter)

    def format(self, record):
        logging.Formatter.format(self, record)
        if not hasattr(record, "extra_info") or record.extra_info["type"] == "app":
            return json.dumps(get_app_log(record))
        elif is_valide_user_data(record):
            return json.dumps(get_access_log(record))
