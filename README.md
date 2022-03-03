# raspberrypi_encoder
Using rotary encoders for Raspberry Pi via dtoverlay. This Python program creates a thread which runs the encoder code in the background once you create the Encoder object! Tested on Raspbian and Ubuntu 20.04.  
On Raspbian the following to the bottom of /boot/config.txt:  
```
dtoverlay = rotary_encoder, pin_a=5, pin_b=6, relative_axis=1   
```
where pin_a is the Channel A, pin_b is your Channel B of your encoder. On Ubuntu please edit /boot/firmware/config.txt.  

To use in your code, first install evdev for Python:
```
pip install evdev
```
Then in your code:

```
import RPIEncoder  
pin_A = 5
ticks_per_revolution = 600  
encoder = RPIEncoder.Encoder(pin_A,ticks_per_revolution)
ticks = encoder.getTicks() # get ticks/pulses
revs = encoder.getRevs() # get revolutions (optional)
```

For a timestamped version, there are two possibilities, each useful in different scenarios:
  
First case -> (time function called, current ticks) = encoder.getTicksStamped()  
Second case -> (time last encoder event, current ticks) = encoder.getTicksStampedAtEvent(), this corresponds to the actual moment the encoder event happened in hardware rather than the time the function is called. 
Similar for revolutions.  

```
import RPIEncoder  
start_time = 0.0
pin_A = 5
ticks_per_revolution = 600  
encoder = RPIEncoder.EncoderStamped(pin_A, ticks_per_revolution, start_time) # or encoder = RPIEncoder.EncoderStamped(pin_A, ticks_per_revolution)
(t1, ticks) = encoder.getTicksStamped() # get ticks/pulses
(t1, revs) = encoder.getRevsStamped() # get revolutions (optional)
(t2, ticks) = encoder.getTicksStampedAtEvent() # get ticks/pulses
(t2, revs) = encoder.getRevsStampedAtEvent() # get revolutions (optional)
```
