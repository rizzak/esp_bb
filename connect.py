import network
import machine
import time
import json


class Connect:
    """For connect to internet"""

    @staticmethod
    def connect():
        """Connect to internet"""
        my_networks = json.loads(open('networks.json').read())
        led2 = machine.Pin(2, machine.Pin.OUT)
        led2.on()
        led16 = machine.Pin(16, machine.Pin.OUT)
        sta_if = network.WLAN(network.STA_IF)

        # scan what’s available
        available_networks = []
        for net in sta_if.scan():
            ssid = net[0].decode("utf-8")
            bssid = net[1]
            strength = net[3]
            available_networks.append(dict(ssid=ssid, bssid=bssid, strength=strength))
        # Sort fields by strongest first in case of multiple SSID access points
        available_networks.sort(key=lambda station: station["strength"], reverse=True)

        if not sta_if.isconnected():
            for config in json.loads(my_networks)['known_networks']:
                for ssid in available_networks:
                    if config["ssid"] == ssid["ssid"]:
                        print('connecting to network {0} ...'.format(config["ssid"]))
                        sta_if.active(True)
                        sta_if.connect(config["ssid"], config["password"])

        while not sta_if.isconnected():
            led16.off()
            time.sleep(1)
            led16.on()
            time.sleep(1)
            pass

        print('network config:', sta_if.ifconfig())
        led2.off()
        time.sleep(0.2)
        led2.on()

    @staticmethod
    def find_known_wifi():
        """Searching known wifi network"""

        pass
