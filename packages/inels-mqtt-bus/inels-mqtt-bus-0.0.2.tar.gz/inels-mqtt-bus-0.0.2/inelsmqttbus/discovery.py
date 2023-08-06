"""Discovery class handle find all devices in the broker and create devices."""
import logging

from . import InelsMqtt
from .device import Device

_LOGGER = logging.getLogger(__name__)

class InelsDiscovery(object):
    """Handles device discovery"""
    
    def __init__(self, mqtt: InelsMqtt) -> None:
        """Initializes inels mqtt discovery"""
        self.__mqtt: InelsMqtt = mqtt,
        self.__devices: list[Device] = []
        
    @property
    def devices(self) -> list[Device]:
        """Returns device list
        
        Returns
            list[Device]: List of devices
        """
        return self.__devices

    def discovery(self) -> list[Device]:
        """Discover and create device list

        Returns:
            list[Device]: status topic -> List of Device object
        """
        devs = self.__mqtt.discovery_all()
        
        devices = []
        
        for item in devs:
            devices.append(Device(item, devs[item]))
        
        return devices
            
            
        