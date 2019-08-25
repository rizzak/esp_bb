import time
import network
import json


from blink import Blink


class Connect:
    """For connect to internet"""

    @staticmethod
    def connect():
        """Connect to internet"""
        my_networks = json.loads(open('config.json').read())
        led16 = Blink(16)
        led2 = Blink(2)
        sta_if = network.WLAN(network.STA_IF)

        sta_if.active(True)

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
            led16.blink(2, 0.2)
            for config in my_networks['known_networks']:
                for ssid in available_networks:
                    if config["ssid"] == ssid["ssid"]:
                        print('connecting to network {0} ...'.format(config["ssid"]))
                        sta_if.active(True)
                        sta_if.connect(config["ssid"], config["password"])
        time.sleep(3)
        print('network config:', sta_if.ifconfig())
        led2.blink(5, 0.03)
        time.sleep(3)

    @staticmethod
    def check_and_reconnect():
        if network.WLAN(network.STA_IF).ifconfig()[0] == '0.0.0.0':
            try:
                Connect.connect()
                print('IP is: ' + network.WLAN(network.STA_IF).ifconfig()[0])
            except:
                pass
