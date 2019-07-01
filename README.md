# esp_bb
esp micropython home automation module

Формат networks.json для перечисления ваших WIFI сетей:
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
    ]
}
```