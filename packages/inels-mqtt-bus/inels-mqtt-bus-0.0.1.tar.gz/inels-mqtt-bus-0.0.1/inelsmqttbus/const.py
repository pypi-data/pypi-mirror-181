"""Constances of inels-mqtt-bus."""
from __future__ import annotations
from typing import Final
from enum import IntEnum, Enum


MQTT_DISCOVER_TOPIC = "inels/status/#"

# FRAGMENT/MQTT CONSTANTS
FRAGMENT_DOMAIN = "fragment_domain"
FRAGMENT_SERIAL_NUMBER = "fragment_serial_number"
FRAGMENT_STATE = "fragment_state"
FRAGMENT_DEVICE_TYPE = "fragment_device_type"
FRAGMENT_UNIQUE_ID = "fragment_unique_id"

MQTT_BROKER_CLIENT_NAME = "inels-mqtt"
MQTT_DISCOVER_TOPIC = "inels/status/#"

TOPIC_FRAGMENTS = {
    FRAGMENT_DOMAIN: 0,
    FRAGMENT_STATE: 1,
    FRAGMENT_SERIAL_NUMBER: 2,
    FRAGMENT_DEVICE_TYPE: 3,
    FRAGMENT_UNIQUE_ID: 4,
}

# DEVICE SPECIFIC INFO
SA3_01B = "SA3-01B"
DA3_22M = "DA3-22M"
GTR3_50 = "GTR3-50"
GSB3_90SX = "GSB3-90Sx"

DEVICE_TYPE_DICT = {
    "100" : SA3_01B,
    "101" : DA3_22M,
    "102" : GTR3_50,
    "103" : GSB3_90SX,
}


# MQTT/INELS CONSTANTS
MQTT_TRANSPORTS = {"tcp", "websockets"}

MQTT_TIMEOUT: Final = "timeout"
MQTT_HOST: Final = "host"
MQTT_USERNAME: Final = "username"
MQTT_PASSWORD: Final = "password"
MQTT_PORT: Final = "port"
MQTT_CLIENT_ID: Final = "client_id"
MQTT_PROTOCOL: Final = "protocol"
MQTT_TRANSPORT: Final = "transport"
PROTO_31 = "3.1"
PROTO_311 = "3.1.1"
PROTO_5 = 5

DISCOVERY_TIMEOUT_IN_SEC = 5

VERSION = "0.1.0"

MANUFACTURER: Final = "ELKO EP s.r.o"
