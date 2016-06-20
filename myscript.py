from urllib2 import urlopen
import time
import platform
import socket

carbensever = '127.0.0.1'
carbenport = 2003
delay = 60

while True:
  url = urlopen("http://192.168.1.160/tstat").read()
  print url

  import json
  j = json.loads(url)
  print "curennt tempriture: %d " %  j['temp']
  print "thremoste oprating mode: %d " %  j['tmode']
  print "target tempriture temporariy override: %d " %  j['override']
  print "target tempriture hold status: %d " %  j['hold']
  print "tempary target heat setpoint: %d " %  j.get('t_heat',0)
  print "tempary target cool setpoint: %d " %  j.get('t_cool',0)

  timestamp = int(time.time())

  lines = [
    'themistat.temp %s %d' % (j['temp'], timestamp),
    'themistat.tmode %s %d' % (j['tmode'], timestamp),
    'themistat.override %s %d' % (j['override'], timestamp),
    'themistat.hold %s %d' % (j['hold'], timestamp),
    'themistat.t_heat %s %d' % (j.get('t_heat'), timestamp),
    'themistat.t_cool %s %d' % (j.get('t_cool'), timestamp),
  ]

  message = '\n'.join(lines) + '\n'
  print message

  sock = socket.socket()
  sock.connect((carbensever, carbenport))
  sock.sendall(message)
  sock.close()

  print "loop end\n\n"

  time.sleep(delay)
