import sys
import socket
from motor import Motor

m = Motor()

html = """<!DOCTYPE html>
<html>
<head> <title>RC Car </title> </head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    html { 
    background-color: #281f55;
    font-family: Roboto,Arial,Helvetica,Helvetica Neue,FreeSans,sans-serif;
    display: inline-block; 
    margin: 0px auto; 
    text-align: center;
    }
    .button:active {
    background-color: #d9063e;
    border-color: #d9063e;
    }
    .button { 
    -webkit-user-select: none; 
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
    background-color: #f8104d;
    border-radius: 3px;
    border-color: #f8104d;
    color: white; 
    padding: 12px 28px; 
    text-decoration: none; 
    font-size: 26px; 
    margin: 1px; 
    cursor: pointer;
    }
</style>

</head>
  <body onmouseup="clearMove()" ontouchend="clearMove()">
    <button class="button" onmousedown="moveForward()" id="forward">FORWARD</button></p>
    <div style="clear: both;">
    <p>
    <button class="button" onmousedown="moveLeft()" ontouchstart="moveLeft()" id="left">LEFT </button>
    <button class="button" onmousedown="moveBack()" ontouchstart="moveBack()" id="back"">BACK</button>
    <button class="button" onmousedown="moveRight()" ontouchstart="moveRight()" id="right">RIGHT</button>
    </p>
    <button onmousedown="repl()" ontouchstart="repl()" id="Repl">Repl</button>
    </div>

    <script>
    var d = "";

    function moveForward(){d = "forward";}
    function moveBack(){d = "back";}
    function moveLeft(){d = "left";}
    function moveRight(){d = "right";}
    function repl(){d = "repl";}

    function clearMove(){
        d = "";
        console.log('stop');
        var xmlhttp=new XMLHttpRequest();
        xmlhttp.open("POST","Val=stopX",true);
        xmlhttp.send();
        }

    function myFunction(){
        if (d) {
            console.log(d);
            var xmlhttp=new XMLHttpRequest();
            xmlhttp.open("POST","Val="+d+"X",true);
            xmlhttp.send();
            }
        }
        
    document.addEventListener('keydown', function(event) {
        switch(event.code) {
            case 'ArrowUp':
                moveForward();
                break;
            case 'ArrowDown':
                moveBack();
                break;
            case 'ArrowLeft':
                moveLeft();
                break;
            case 'ArrowRight':
                moveRight();
                break;
        }
    });
    
    document.addEventListener('keyup', function(event) {
        if (event.code == 'ArrowUp' || event.code == 'ArrowDown' || event.code == 'ArrowLeft' || event.code == 'ArrowRight') {
            clearMove()
        }
    });
    
    setInterval(myFunction, 200);

    </script>
  </body>
</html>
"""
data = 0


class Webserver():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 80))
        self.s.listen(5)

    def start(self):
        while True:
            conn, addr = self.s.accept()
            request = str(conn.recv(1024))

            if request:
                ia = request.find("Val=")
                ib = request.find("X")
                direction = request[ia + 4:ib]
                print(direction)
                if direction == 'forward':
                    m.forward()
                elif direction == 'back':
                    m.reverse()
                elif direction == 'left':
                    m.left()
                elif direction == 'right':
                    m.right()
                elif direction == 'stop':
                    m.stop()
                elif direction == 'repl':
                    sys.exit()

            conn.sendall(html.encode())
            conn.sendall('\n'.encode())
            conn.close()
