from math import sqrt, sin
from Numeric import *
from RandomArray import random, randint, normal
from presto import rfft, TWOPI, spectralpower
from Pgplot import plotxy, plotbinned, closeplot
from Statistics import average, standardDeviation, histogram

# This code tests the statistics of photon based power
# spectra and signals.  It is useful for checking
# x-ray statistics equations...

N = 2**14               # Number of points in FFT
numphot = 5000          # Number of photons in time series
pfract = 0.2            # Number of pulsed cts / number of background cts
freq = N/4              # Signal Fourier Frequency (hz)
phase = 0.5             # Initial pulse phase (0.0-1.0)
pulsetype = 'Sine'      # Can be either 'Sine' or 'Gaussian'
width = 0.1             # +/-1 sigma width of Gaussian pulse in phase

data = zeros(N, 'f')
data.savespace()
pulsedphot = int(pfract * numphot)
backgdphot = numphot - pulsedphot
# Place the non-pulsed photons
points = randint(0, N, backgdphot)
for point in points:
    data[point] = data[point] + 1.0
del(points)
# Place the pulsed photons
pulses = randint(0, freq, pulsedphot)
if pulsetype=='Sine':
    x = arange(10001, typecode='d') * TWOPI/10000
    coscdf = (x + sin(x))/TWOPI
    uvar = random(pulsedphot)
    phases = take((x + TWOPI * phase) % TWOPI,
                  searchsorted(coscdf, uvar)) / TWOPI
    #plotxy(coscdf, x)
    #closeplot()
    #hist = histogram(phases, 100, [0.0, TWOPI])
    #plotbinned(hist[:,1], hist[:,0])
    #closeplot()
elif pulsetype=='Gaussian':
    phases = normal(0.0, width, pulsedphot) % 1.0 + phase
points = ((pulses + phases) / freq * N).astype('i')
for point in points:
    data[point] = data[point] + 1.0
tmp = average(data)
#print 'Average Data = ', tmp
#print '   sqrt(avg) = ', sqrt(tmp)
#print ' StdDev Data = ', standardDeviation(data)
ft = rfft(data)
pows = spectralpower(ft)/ft[0].real
pows[0] = 1.0
#print 'Number of counts =', sum(data)
#print 'Max power =', max(pows)
#print 'Max  freq =', argmax(pows)
theo_pow = pfract**2.0*numphot/4.0
meas_pow = pows[freq]
print 'Theo pow =', theo_pow
print 'Meas pow =', meas_pow
#print 'Theo pow2 (pfract^2Nph/(4)) = ', theo_pow
#plotxy(pows)
#closeplot()
del(points)