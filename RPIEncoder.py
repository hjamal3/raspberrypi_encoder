import evdev
import select
import threading

# an encoder class that returns the number of ticks and optionally revolutions
# example:
# ticks_per_revolution = 600
# e = Encoder(ticks_per_revolution) 
# print(e.revs())
# print(e.ticks)
# or 
# e = Encoder()
# print(e.ticks)
class Encoder:
  def __init__(self, ticks_per_rev = 1):
    self.ticks_per_rev = ticks_per_rev
    self.ticks = 0
    self.encoder_exec_thread = threading.Thread(target=self.exec, name="encoder_exec_thread")
    self.encoder_exec_thread.start()

  def exec(self):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    devices = {dev.fd: dev for dev in devices}
    self.ticks = 0
    print("Value: {0}".format(self.ticks))
    while True:
      r, w, x = select.select(devices, [], [])
      for fd in r:
        for event in devices[fd].read():
          event = evdev.util.categorize(event)
          if isinstance(event, evdev.events.RelEvent):
            self.ticks = self.ticks + event.event.value

  def revs(self):
    return self.ticks/self.ticks_per_rev

  def __del__(self):
    # body of destructor
    self.encoder_exec_thread.join()