import evdev
import select
import threading
from timeit import default_timer as timer
import time

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
# start_time = 0 # seconds
# e = EncoderStamped(pin_a, ticks_per_rev, start_time)
# (t, ticks) = e.getTicksStamped()
# (t_latest_tick, ticks) = e.getTicksStampedAtEvent()
class EncoderStamped:

  ticks = 0
  mutex = threading.Lock()

  def __init__(self, pin_a, ticks_per_rev = 1, start_offset=0):
    self.ticks_per_rev = ticks_per_rev
    self.start_time = start_offset # offset from 0 seconds
    
    self.start = timer() # used to measure time to getter
    self.start_epoch = time.time() # used to measure time to event itself
    self.event_time = self.start_epoch
  
    self.device = evdev.InputDevice('/dev/input/by-path/platform-rotary@'
                               + str(hex(pin_a)[2:]) + '-event')
    self.encoder_exec_thread = threading.Thread(target=self.exec, name="encoder_exec_thread")
    self.encoder_exec_thread.start()

  def exec(self):
    print("EncoderStamped started.")
    for event in self.device.read_loop():
        if event.type == evdev.ecodes.EV_REL:
            self.mutex.acquire()
            self.ticks = self.ticks + event.value
            self.event_time = event.timestamp()
            self.mutex.release()

  def getRevs(self):
    return self.ticks/self.ticks_per_rev

  def getTicks(self):
    return self.ticks

  # returns time in seconds from constructor till now and total revolutions 
  def getRevsStamped(self):
    return (self.start_time+timer()-self.start, self.ticks/self.ticks_per_rev)

  # returns time in seconds from constructor till now and total ticks 
  def getTicksStamped(self):
    return (self.start_time+timer()-self.start, self.ticks)

  # returns time in seconds from constructor till last event (interrupt) and total revolutions 
  def getRevsStampedAtEvent(self):
    self.mutex.acquire()
    out = (self.start_time+(self.event_time-self.start_epoch), self.ticks/self.ticks_per_rev)
    self.mutex.release()
    return out

  # returns time in seconds from constructor till last event (interrupt) and total ticks 
  def getTicksStampedAtEvent(self):
    self.mutex.acquire()
    out = (self.start_time+timer()+(self.event_time-self.start_epoch), self.ticks)
    self.mutex.release()
    return out

  def __del__(self):
    # body of destructor
    self.encoder_exec_thread.join()