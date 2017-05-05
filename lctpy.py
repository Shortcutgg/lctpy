from __future__ import print_function
from threading import Thread, Lock
from zipfile import ZipFile
import keyboard
import time
import click
import datetime
import os
import requests

basedir = ".lct"

def createfile():
   if not os.path.isdir(basedir):
      os.mkdir(basedir)
   ts = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
   print("Creating file", ts)
   return open(os.path.join(basedir, str(ts + ".txt")), 'w+')


glock = Lock()
current_file = createfile()

def savekey(down, num):
   glock.acquire()
   ts = datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
   line = ('{0} - {1} - {2}'.format("P" if down else "R", num, ts))
   print(line, file=current_file)
   glock.release()

class worker(Thread):
   def __init__(self, device):
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
      if ke.device == self.device:
         if ke.event_type == 'down':
            self.keydown(ke)
         else:
            self.keyup(ke)

   def run(self):
      keyboard.hook(self.process)
      while True:
         time.sleep(1)

class uploader(Thread):
   def __init__(self, server, port, email, interval):
      self.server = server
      self.port = port
      self.email = email
      self.interval = interval
      super(uploader, self).__init__()

   def pack(self):
      global current_file
      glock.acquire()
      current_file.close()
      current_file = createfile()
      glock.release()

      ignore_file = os.path.basename(current_file.name)

      for filename in os.listdir(basedir):
         if filename.endswith("txt") and not filename == ignore_file:
            print("Packing", filename)
            full_filename = os.path.join(basedir, filename)
            size = os.stat(full_filename).st_size
            if size > 0:
               with ZipFile(os.path.join(basedir, filename[:-4] + ".zip"), 'w') as z:
                  z.write(full_filename, filename)
            os.remove(full_filename)

   def upload(self):
      url = "http://{0}:{1}/".format(self.server, self.port)
      for filename in os.listdir(basedir):
         if filename.endswith("zip"):
            print("Uploading", filename)
            full_filename = os.path.join(basedir, filename)
            f = open(full_filename, 'rb')
            files = {'file': f}
            payload = { 'user_id' : self.email }
            rv = requests.post(url, data=payload, files=files)
            print("Uploaded", filename, "-", str(os.stat(full_filename).st_size) + "bytes", "/", rv.status_code)
            f.close()
            if rv.status_code == 205:
               os.remove(full_filename)

   def run(self):
      while True:
         time.sleep(self.interval)
         self.pack()
         self.upload()

default_server = 'lc.shortcut.gg'
default_port = 8001
default_device = '/dev/input/by-id/usb-qmkbuilder_keyboard-event-kbd'
default_interval = 900 # 15 mins

@click.command()
@click.option('--server',
              default=default_server,
              help='Address of the server (default {0})'.format(default_server))
@click.option('--port',
              default=default_port,
              help='Port on the server (default {0})'.format(default_port))
@click.option('--email',
              prompt='Your email',
              help='Your Shortcut community email address')
@click.option('--device',
              default=default_device,
              help='The device to hook (default {0})'.format(default_device))
@click.option('--interval',
              default=default_interval,
              help='Interval in seconds between uploads (default {0})'.format(default_interval))
def run(server, port, email, device, interval):
   justify = 10
   print("Server".ljust(justify), server)
   print("Port:".ljust(justify), port)
   print("Email:".ljust(justify), email)
   print("Device:".ljust(justify), device)
   print("Interval:".ljust(justify), interval)
   print("-----------------")
   worker(device).start()
   uploader(server, port, email, interval).start()

if __name__ == '__main__':
   run()
