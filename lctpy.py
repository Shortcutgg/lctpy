from __future__ import print_function
import keyboard
import time
import click

from threading import Thread

def hookcb(ke):
   print (ke, ke.device)

class worker(Thread):
   def run(self):
      keyboard.hook(hookcb)
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
   worker().start()

if __name__ == '__main__':
   run()
