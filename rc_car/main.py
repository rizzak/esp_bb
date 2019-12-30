from web_server import Webserver
try:
    w=Webserver()
except OSError:
    import machine
    machine.reset()
    print('OSError, im do machine.restart()')
w.start()
