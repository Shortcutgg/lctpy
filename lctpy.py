from __future__ import print_function
from threading import Thread, Lock
import keyboard
import time
import click
import datetime

glock = Lock()
lines = []

def addline(line):
   glock.acquire()
   lines.append(line)
   glock.release()

def savekey(down, num):
   ts = datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
   line = ('{0} - {1} - {2}'.format("P" if down else "R", num, ts))
   print(line)
   addline(line)

class worker(Thread):
   def __init__(self, server, port, email, device):
      self.server = server
      self.port = port
      self.email = email
      self.device = device
      self.keys = {}
      self.count = 0
      super(worker, self).__init__()

   def keydown(self, ke):
      if ke.scan_code not in self.keys:
         self.count += 1
         self.keys[ke.scan_code] = self.count
         savekey(True, self.count)

   def keyup(self, ke):
      if ke.scan_code in self.keys:
         savekey(False, self.keys[ke.scan_code])
         del self.keys[ke.scan_code]

   def process(self, ke):
      if ke.event_type == 'down':
         self.keydown(ke)
      else:
         self.keyup(ke)

   def run(self):
      keyboard.hook(self.process)
      while True:
         time.sleep(1)



@click.command()
@click.option('--server', default="lc.shortcut.gg", help='Address of the server')
@click.option('--port', default="8001", help='Port on the server')
@click.option('--email', prompt='Your email', help='Your Shortcut community email address')
@click.option('--device', default='/dev/input/by-id/usb-qmkbuilder_keyboard-event-kbd',
              help='The device to hook')
def run(server, port, email, device):
   print("Server:\t", server)
   print("Port:\t", port)
   print("Email:\t", email)
   print("Device:\t", device)
   print("-----------------")
   worker(server, port, email, device).start()

if __name__ == '__main__':
   run()
