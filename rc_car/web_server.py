import sys
import socket
from motor import Motor
from time import time

m = Motor()

html = open('html/index.html', 'r').read()
data = 0
speed = 1023


class Webserver():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 80))
        self.s.listen(5)

    def start(self):
        left_old = 0
        right_old = 0
        last_request_time = time()

        while True:
            try:
                conn, addr = self.s.accept()
                request = str(conn.recv(1024))

                if request:
                    if request.find('GET') != -1:
                        conn.sendall(html.encode())
                    else:
                        last_request_time = time()
                        ia = request.find("#")
                        ib = request.find("$")

                        if ia != -1:
                            power, direction = map(int, request[ia + 1:ib].split('~'))
                            left = speed * power // 100
                            right = left

                            if direction == 1:
                                if right == 0:
                                    left = speed
                                    right = -speed
                                else:
                                    right //= 3
                            elif direction == -1:
                                if left == 0:
                                    right = speed
                                    left = -speed
                                else:
                                    left //= 3
                            if left != left_old or right != right_old:
                                print(left, right)
                                m.move(left, right)
                                left_old, right_old = left, right

                conn.sendall('\n'.encode())
                conn.close()

            except Exception as inst:
                print(inst)

            if time() - last_request_time > 2:
                m.stop()
            
