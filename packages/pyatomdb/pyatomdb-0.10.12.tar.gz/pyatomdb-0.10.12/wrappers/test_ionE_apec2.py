import xspec
import IonE_apec_xspec
import pylab
import numpy

m1 = xspec.Model('pyibvvapec')

xspec.AllData.dummyrsp(lowE=0.3,highE=2.0, nBins=67001)
string="0.0, , 0.0, 0.2,100,1000"
m1.pyibvvapec.H=string
m1.pyibvvapec.He=string
m1.pyibvvapec.Li=string
m1.pyibvvapec.Be=string
m1.pyibvvapec.B=string
m1.pyibvvapec.C=string
m1.pyibvvapec.N=string
m1.pyibvvapec.O=string
m1.pyibvvapec.F=string
m1.pyibvvapec.Ne=string
m1.pyibvvapec.Na=string
m1.pyibvvapec.Mg=string
m1.pyibvvapec.Al=string
m1.pyibvvapec.Si=string
m1.pyibvvapec.P=string
m1.pyibvvapec.S=string
m1.pyibvvapec.Cl=string
m1.pyibvvapec.Ar=string
m1.pyibvvapec.K=string
m1.pyibvvapec.Ca=string
m1.pyibvvapec.Sc=string
m1.pyibvvapec.Ti=string
m1.pyibvvapec.V=string
m1.pyibvvapec.Cr=string
m1.pyibvvapec.Mn=string
m1.pyibvvapec.Fe=string
m1.pyibvvapec.Co=string
m1.pyibvvapec.Ni=string

fig= pylab.figure()
fig.show()
ax = fig.add_subplot(111)


xspec.Plot.xAxis='keV'
y={}
for i in [6,8,10,12,14,18,26]:
  if i == 6:
    k=m1.pyibvvapec.C
  if i == 8:
    k=m1.pyibvvapec.O
  if i == 10:
    k=m1.pyibvvapec.Ne
  if i == 12:
    k=m1.pyibvvapec.Mg
  if i == 14:
    k=m1.pyibvvapec.Si
  if i == 18:
    k=m1.pyibvvapec.Ar
  if i == 26:
    k=m1.pyibvvapec.Fe
  
  k.values='1.0'

  xspec.Plot('model')
  k.values='0.0'
  if i==6:
    x1= numpy.array(xspec.Plot.x())

  y[i] = numpy.array(xspec.Plot.model())

# change the thermal broadening

  ax.plot(x1,y[i], label=repr(i))


ax.legend(loc=0)
pylab.draw()
zzz=input()
