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

    @property
    def mqtt(self) -> InelsMqtt:
        """Returns Mqtt client
        
        Returns
            InelsMqtt: mqtt client
        """
        return self.__mqtt
    
    def discovery(self) -> None:
        """Discover and create device list

        Returns:
            list[Device]: status topic -> List of Device object
        """
        A = InelsMqtt(self.mqtt)
        devs = A.discovery_all()
        #devs = self.__mqtt.discovery_all()
        #TODO fix
        
        devices : list[Device] = []
        
        for item in devs:
            devices.append(Device(item, devs[item]))
        
        self.__devices = devices
            
            
        