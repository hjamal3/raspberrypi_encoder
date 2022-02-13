# raspberrypi_encoder
Using encoders for Raspberry Pi via dtoverlay. This Python program creates a thread which runs the encoder code in the background once you create the Encoder object!  
Add the following to /boot/config.txt:  
```
dtoverlay = rotary_encoder, pin_a=5, pin_b=6, relative_axis=1   
```
where pin_a is the Channel A, pin_b is your Channel B of your encoder.

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

For a timestamped version:
```
import RPIEncoder  
start_time = 0.0
pin_A = 5
ticks_per_revolution = 600  
encoder = RPIEncoder.EncoderStamped(pin_A, ticks_per_revolution, start_time) # or encoder = RPIEncoder.EncoderStamped(pin_A, ticks_per_revolution)
(t, ticks) = encoder.getTicksStamped() # get ticks/pulses
(t, revs) = encoder.getRevs() # get revolutions (optional)
```
