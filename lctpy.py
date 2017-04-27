import keyboard
import time
import click

from threading import Thread

def hookcb(ke):
   print (ke)

class worker(Thread):
   def run(self):
      keyboard.hook(hookcb)
      while True:
         time.sleep(1)

@click.command()
@click.option('--server', default="lc.shortcut.gg", help='Address of the server')
@click.option('--port', default="8001", help='Port on the server')
@click.option('--email', prompt='Your email', help='Your Shortcut community email address')
def run(server, port, email):
   print("Server:", server)
   print("Port:", port)
   print("Email:", email)
   worker().start()

if __name__ == '__main__':
   run()
