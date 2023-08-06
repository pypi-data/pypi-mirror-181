
from inelsmqttbus import InelsMqtt
from .const import (
    Platform,
    TOPIC_FRAGMENTS,
    FRAGMENT_DEVICE_TYPE,
    DEVICE_TYPE_DICT,
    FRAGMENT_UNIQUE_ID,
    DEVICE_PLATFORM_DICT,
)

class Device(object):
    """Carry basic device stuff

    Args:
        object (_type_): default object it is new style of python class coding
    """
    def __init__(
        self,
        mqtt: InelsMqtt,
        state_topic: str,
        status_value: str,
    ) -> None:
        fragments = state_topic.split("/")

        self.__mqtt: InelsMqtt = mqtt

        self.__platforms : list[Platform] = DEVICE_PLATFORM_DICT[
            fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
        ]
        self.__dev_type : str = DEVICE_TYPE_DICT[
            fragments[TOPIC_FRAGMENTS[FRAGMENT_DEVICE_TYPE]]
        ]
        self.__dev_address : str = fragments[
            TOPIC_FRAGMENTS[FRAGMENT_UNIQUE_ID]
        ]
        self.__state_topic: str = state_topic
        self.__status_value: str = status_value

    @property
    def mqtt(self) -> InelsMqtt:
        """Returns mqtt client"""
        return self.__mqtt

    @property
    def platforms(self) -> list[Platform]:
        """Returns entity platforms used by device"""
        return self.__platforms

    @property
    def dev_type(self) -> str:
        """Returns physical device type number"""
        return self.__dev_type

    @property
    def dev_address(self) -> str:
        """Returns physical device address"""
        return self.__dev_address

    @property
    def state_topic(self) -> str:
        """Returns state topic"""
        return self.__state_topic

    @property
    def status_value(self) -> str:
        """Returns status value"""
        return self.__status_value
