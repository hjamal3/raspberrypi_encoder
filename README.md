# raspberrypi_encoder
Using encoders for Raspberry Pi via dtoverlay. This Python program creates a thread which runs the encoder code in the background once you create the Encoder object!  
Add the following to /boot/config.txt:  
```
dtoverlay=rotary_encoder,pin_a=5,pin_b=6,relative_axis=1   
```
where pin_a is the Channel A, pin_b is your Channel B of your encoder.

To use in your code:  
```
import RPIEncoder  
ticks_per_revolution = 600  
encoder = RPIEncoder.Encoder(ticks_per_revolution) # or RPIEncoder.Encoder() defaults to ticks_per_revolution = 1
t = encoder.getTicks() # get ticks/pulses
d = encoder.getRevs() # get revolutions (optional)

```
