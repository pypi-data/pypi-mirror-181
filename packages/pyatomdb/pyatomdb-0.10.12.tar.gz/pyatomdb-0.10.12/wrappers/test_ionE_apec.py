import xspec
import IonE_apec_xspec
import pylab
import numpy

m1 = xspec.Model('pyibapec')

xspec.AllData.dummyrsp(lowE=0.3,highE=2.0, nBins=6701)

xspec.Plot.xAxis='keV'
xspec.Plot('model')

x1= numpy.array(xspec.Plot.x())
y1 = numpy.array(xspec.Plot.model())

# change the thermal broadening

m1.pyibapec.kTlwidth=0.01
xspec.Plot('model')
y2 = numpy.array(xspec.Plot.model())

m1.pyibapec.kTlwidth=10.
xspec.Plot('model')
y3 = numpy.array(xspec.Plot.model())

fig= pylab.figure()
fig.show()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212, sharex=ax)
ax.plot(x1,y2, label='kTline=0.1')
ax.plot(x1,y3, label='kTline=10.0')
ax.plot(x1,y1, label='kTline=1.0')


ax2.plot(x1,y2/y1, label='0.1/1.0')
ax2.plot(x1,y3/y1, label='10.0/1.0')

ax.legend(loc=0)
pylab.draw()
zzz=input()



#
