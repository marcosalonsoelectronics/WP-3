# -*- coding: utf-8 -*-
"""
How to generate Bode Plots
Example with buck converter
Marcos Alonso
marcos@uniovi.es
"""
from math import pi, log10
from control import tf, bode_plot, margin, step_response
import matplotlib.pyplot as plt
# Create Laplace variable
s = tf('s')
# Buck converter parameters
Vi=10; Vo=5; RL=1; D=0.5
L=50e-6; rl=0.05; C=10e-6; rc=0.15
# Ramp peak-to-peak voltage
Vpp=10
# Plant's frequency response
Gp=(1/Vpp)*(Vo/D)*(1+rc*C*s) / ( L*C*(1+rc/RL)*s**2 + \
                        (L/RL + rc*C + rl*C + rl*rc*C/RL)*s + 1 + rl/RL )
# Plot Plant's Bode
# Note that one Hz is true, omega_limits are in Hz
# bode_plot(Gp, dB=True, Hz=True, omega_limits=(10, 1e6), omega_num=100 )

mag, phase, omega = bode_plot(Gp, dB=True, Hz=True, omega_limits=(10, 1e6), \
                              omega_num=100 )
i=70
print(omega[i]/2/pi, 20*log10(mag[i]), phase[i]*180/pi)
   
#%% New Cell for Compensator Plotting
# Compensator
R1= 2.24e3; R2= 2.24e3; C2= 10e-9
C= (1 + R2*C2*s)/( R1*C2*s )
bode_plot(C, dB=True, Hz=True, omega_limits=(10, 1e6), omega_num=100)


#%% New Cell for Loop Gain Plotting
# Sensor
H=1
# Loop gain
T= Gp*C*H
# Plot loop gain Bode
bode_plot(T, dB=True, Hz=True, omega_limits=(10, 1e6), omega_num=100, \
          margins=False)
# Get gain margin (gm), phase margin (pm)
# Frequency for gain margin (phase=-180) (wcg)
# Frequency for phase margin (gain= 0dB) (wcp)
gm, pm, wcg, wcp = margin(T)
print ("Phase margin= ", pm)
print ("Crossover frequency (0 dB)= ", wcp/(2*pi));

#%% New cell for closed loop response
# Closed loop response
Gcl = C*Gp/(1 + C*Gp*H)
mag1, phase1, omega1 = bode_plot(Gcl, dB=True, Hz=True, \
                                  omega_limits=(10, 1e6), omega_num=100)
i=50
print(omega1[i]/2/pi, 20*log10(mag1[i]), phase1[i]*180/pi)

#%% New cell for step response plotting
# Returns: T, time array; yout, output array
Time, yout = step_response(Gcl)
# Plot results
plt.figure(2)
plt.plot(Time*1000, yout, 'blue')
plt.grid(True)
plt.xlabel("Time (ms)")
plt.ylabel("Output voltage (V)")























