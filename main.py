import ubinasciiimport machineimport timefrom temperature import TemperatureSensorfrom temperature_client import TemperatureClientclient_id = ubinascii.hexlify(machine.unique_id())sensor = TemperatureSensor(5)# tc = TemperatureClient(client_id, '93.80.147.216', 5, topic='esp/temp')# tc.start(60)while True:    print(str(time.localtime()) + ' | temp: ' + str(sensor.read_temp()))    time.sleep(60)