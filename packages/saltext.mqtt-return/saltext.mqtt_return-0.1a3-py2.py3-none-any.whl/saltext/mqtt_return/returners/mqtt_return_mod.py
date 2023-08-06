"""
Salt returner module
"""
import logging
from typing import Any

import handlers.awsiot as awsiot
import handlers.mqtt as mqtt
import salt.returners

log = logging.getLogger(__name__)

__virtualname__ = "mqtt_return"


def __virtual__():
    return __virtualname__


def _get_options(ret=None):
    defaults = {
        "endpoint": "localhost",
        "port": 1883,
        "output": "mqtt",
        "client_id": "salt-master",
    }

    attrs = {
        "endpoint": "endpoint",
        "port": "port",
        "output": "output",
        "topic_prefix": "",
        "aws_access_key_id": "aws_access_key_id",
        "aws_secret_access_key": "aws_secret_access_key",
        "aws_region": "aws_region",
        "client_id": "client_id",
    }

    _options = salt.returners.get_returner_options(
        f"returner.{__virtualname__}",
        ret,
        attrs,
        __salt__=__salt__,
        __opts__=__opts__,
        defaults=defaults,
    )
    # Ensure port is an int
    if "port" in _options:
        _options["port"] = int(_options["port"])
    return _options


def event_return(events):
    _options = _get_options()

    handler = _get_handler(_options)

    for event in events:
        topic = event.get("tag", "")
        data = event.get("data", "")

        # Add prefix if specified
        if _options.get("topic_prefix"):
            topic = f"{_options.get('topic_prefix')}/{topic}"

        try:
            handler(
                opts=_options,
                topic=topic,
                data=data,
            )
        except Exception as error:
            log.error(data)
            log.error(error)


def _get_handler(opts) -> Any:
    if opts.get("output") == "mqtt":
        return mqtt.publish
    elif opts.get("output") == "awsiot":
        return awsiot.publish
