"""Discovery class handle find all devices in the broker and create devices."""
import logging
from typing import Any


from inelsmqttbus import InelsMqtt
from inelsmqttbus.device import Device

_LOGGER = logging.getLogger(__name__)

class InelsDiscovery(object):
    """Handles device discovery"""
    def __init__(self, mqtt: InelsMqtt) -> None:
        """Initializes inels mqtt discovery"""
        self.__mqtt: InelsMqtt = mqtt
        self.__devices: list[Device] = []
        
    @property
    def devices(self) -> list[Device]:
        """Returns device list
        
        Returns
            list[Device]: List of devices
        """
        return self.__devices

    @property
    def mqtt(self) -> InelsMqtt:
        """Returns Mqtt client
        
        Returns
            InelsMqtt: mqtt client
        """
        return self.__mqtt
    
    def discovery(self) -> dict[str, list[Any]]:
        """Discover and create device list

        Returns:
            list[Device]: status topic -> List of Device object
        """
        devs = self.__mqtt.discovery_all()
        
        devices : list[Device] = []
        
        for item in devs:
            devices.append(Device(self.mqtt, item, devs[item]))
        
        self.__devices = devices
            
            
        