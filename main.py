import ubinasciiimport timeimport machineimport jsonfrom blink import Blinkfrom temperature import TemperatureSensorfrom temperature_client import TemperatureClientconfig = json.loads(open('config.json').read())client_id = ubinascii.hexlify(machine.unique_id())sensor = TemperatureSensor(5)led = Blink(16)tc = TemperatureClient(client_id, config['broker_ip'], 5, topic='esp/temp')while True:    try:        tc.publishTemperature()        print(str(time.localtime()) + ' | temp: ' + str(sensor.read_temp()))        led.blink(2, 0.2)    except:        pass    time.sleep(60)