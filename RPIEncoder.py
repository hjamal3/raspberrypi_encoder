import evdev
import select
import threading
from timeit import default_timer as timer

# an encoder class that returns the number of ticks and optionally revolutions
# pin_a: gpio pin channel A of encoder is connected to
# ticks_per_rev: ticks/pulses per revolution of encoder
# ex:
# ticks_per_revolution = 600
# pin_a = 5
# e = Encoder(pin_a, ticks_per_revolution) 
# print(e.getRevs())
# print(e.getTicks())
# or 
# e = Encoder(pin_a)
# print(e.getTicks())
class Encoder:
  def __init__(self, pin_a, ticks_per_rev = 1):
    self.ticks_per_rev = ticks_per_rev
    self.ticks = 0
    self.device = evdev.InputDevice('/dev/input/by-path/platform-rotary@'
                               + str(hex(pin_a)[2:]) + '-event')
    self.encoder_exec_thread = threading.Thread(target=self.exec, name="encoder_exec_thread")
    self.encoder_exec_thread.start()

  def exec(self):
    print("Encoder started.")
    self.ticks = 0
    for event in self.device.read_loop():
        if event.type == evdev.ecodes.EV_REL:
            self.ticks = self.ticks + event.value

  def getRevs(self):
    return self.ticks/self.ticks_per_rev

  def getTicks(self):
    return self.ticks

  def __del__(self):
    # body of destructor
    self.encoder_exec_thread.join()

# a timestamped version of the above
# ex:
# pin_a = 5
# ticks_per_rev = 600
# start_time = 0
# e = EncoderStamped(pin_a, ticks_per_rev, start_time)
# (t, ticks) = e.getTicksStamped()
class EncoderStamped:
  def __init__(self, pin_a, ticks_per_rev = 1, start_time=0):
    self.ticks_per_rev = ticks_per_rev
    self.ticks = 0
    self.start_time = start_time
    self.start = timer()
    self.device = evdev.InputDevice('/dev/input/by-path/platform-rotary@'
                               + str(hex(pin_a)[2:]) + '-event')
    self.encoder_exec_thread = threading.Thread(target=self.exec, name="encoder_exec_thread")
    self.encoder_exec_thread.start()

  def exec(self):
    print("EncoderStamped started.")
    self.ticks = 0
    for event in self.device.read_loop():
        if event.type == evdev.ecodes.EV_REL:
            self.ticks = self.ticks + event.value

  def getRevs(self):
    return self.ticks/self.ticks_per_rev

  def getTicks(self):
    return self.ticks

  def getRevsStamped(self):
    return (self.start_time+timer()-self.start, self.ticks/self.ticks_per_rev)

  def getTicksStamped(self):
    return (self.start_time+timer()-self.start, self.ticks)

  def __del__(self):
    # body of destructor
    self.encoder_exec_thread.join()