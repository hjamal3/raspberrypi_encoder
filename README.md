# raspberrypi_encoder
Using encoders for Raspberry Pi via dtoverlay
Add the following to /boot/config.txt:
dtoverlay=rotary_encoder,pin_a=5,pin_b=6,relative_axis=1  
pin_a is the Channel A, pin_b is your Channel B of your encoder.

To use in your code:  
import RPIEncoder  
ticks_per_revolution = 600  
encoder = RPIEncoder.Encoder(ticks_per_revolution) # or RPIEncoder.Encoder()    
d = encoder.depth() # get depth  
t = encoder.ticks() # get ticks/pulses  
