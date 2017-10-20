from roombaclass import Roomba
import BaseHTTPServer
import socket
import urlparse
import time

robot = Roomba()
robot.wake()
time.sleep(1)

droid.startActivity('android.intent.action.VIEW', 'skype:daniel@bachfeld.com')

HOST_NAME   = ''
PORT_NUMBER = 9090

PAGE_TEMPLATE = '''
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>Remote Control</title>
<style type="text/css">
#action {
background:yellow;
border:0px solid #555;
color:#555;
width:0px;
height:0px;
padding:0px;
}
</style>
<script>
function AddText(text)
{
document.myform.action.value=text;
}
</script>
</head>
<body>
<form name="myform" method="get">
<textarea id="action" name="action">start</textarea>
<input id="button1" type="submit" value="Start" OnClick='javascript:AddText ("start")' />
<input id="button2" type="submit" value="Stop"  OnClick='javascript:AddText ("stop")'  />
<input id="button3" type="submit" value="Back"  OnClick='javascript:AddText ("back")'  />
<input id="button4" type="submit" value="Left"  OnClick='javascript:AddText ("left")'  />
<input id="button5" type="submit" value="Right" OnClick='javascript:AddText ("right")' />
</form>
</body>
</html>
'''


def play( id ):
  if   (id=='start'):
    print ("forward")
    goForward()	
  elif (id=='back'):
    print ("back")
    goBackward()
  elif (id=='left'):
    print ("left")
    spinLeft()
  elif (id=='right'):
    print ("right")
    spinRight()	
  elif (id=='stop'):
    print ("stop")
    stopMoving()

class DroidHandler(BaseHTTPServer.BaseHTTPRequestHandler): 

  def do_HEAD(s): 
    s.send_response(200)
    s.send_header("Content-type", "text/html; charset=utf-8")
    s.end_headers()

  def do_GET(s):
    s.send_response(200)

    my_full_addr = s.headers.get('Host') 
    my_addr = my_full_addr.split(":",2)
    my_ip_addr = my_addr[0]

    url = urlparse.urlsplit(s.path) 
    print url.path
    query = url.query 
    args = urlparse.parse_qsl(query)

    action = '' 
    for arg in args:
      if arg[0] == 'action':
        action = arg[1].strip().replace('\r', '')
        print(action)
        play(action)
        break

    #html = PAGE_TEMPLATE_B
    #s.wfile.write(html)
  

    s.send_header("Content-type", "text/html; charset=utf-8")
    s.end_headers()

    html = PAGE_TEMPLATE
    s.wfile.write(html)

print 'web server running on port %s' % PORT_NUMBER
droid.wakeLockAcquireBright()
my_srv = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), DroidHandler)
my_srv.serve_forever()
