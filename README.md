# esp_bb
esp micropython home automation module

Формат config.json:
```python
{
    "known_networks": [
        {
            "ssid": "Network_name1",
            "password": "password1"
        },
        {
            "ssid": "Network_name2",
            "password": "password2"
        }
    ],
    "broker_ip": "192.168.1.24"
}
```