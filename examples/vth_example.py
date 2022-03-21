"""
Example: fitting thermal + thick target model to STIX spectrum

Before running this script, it is neccessary to run the following commands in a terminal:

export HEADAS=/home/stix_public/Documents/heasoft-6.29/x86_64-pc-linux-gnu-libc2.31
. $HEADAS/headas-init.sh


run this script from the sunxspex/examples/example_data directory of https://github.com/elastufka/sunxspex

eg:
%%bash
conda activate py37 #scientific python environment
cd ~/Solar/sunxspex/examples/example_data
python ../pyxspec_example.py

"""
from astropy.io import fits
from sunxspex import sun_xspec
import time
import xspec
from sunxspex import thermal
import numpy as np
from astropy import units as u
from matplotlib import pyplot as plt
#import logging

#logging.basicConfig(filename='pyxspec_example.log', level=logging.DEBUG)

t0=time.time()
therm=sun_xspec.ThermalModel()
therm.print_ParInfo()

#print("Compare results from thermal.thermal_emission() and sun_xspec.ThermalModel")
#
#edges=np.linspace(5,20,100)
#flux=np.zeros(99)
#params=(5,3,1.,1)
#therm.model(edges,params,flux)
#
#tflux=thermal.thermal_emission(edges*u.keV,emission_measure=5e49/((u.cm)**3),temperature=34813554.36465024*u.K)
#
#fig,ax=plt.subplots()
#ax.plot(edges[1:],flux.flatten())
#ax.plot(edges[1:],tflux)
#ax.set_yscale('log')
#fig.show()

xspec.AllModels.addPyMod(therm.model, therm.ParInfo, 'add')
xspec.AllData.clear()

xspec.AllData("1:1 stx_spectrum_20210908_1712.fits{13}")
xspec.Xset.abund="file feld92a_coronal0.txt"

fit1start=2.0 #keV
fit1end=10.0 #keV
print(f"Fitting with single thermal model initially over range {fit1start}-{fit1end} keV")

m1=xspec.Model('vth')
m1.show()

xspec.AllData.ignore(f"0.-{fit1start} {fit1end}-**")
xspec.Fit.statMethod = "chi"
xspec.Fit.nIterations=100
tstart=time.time()
xspec.Fit.perform()
print(f"Single thermal fit took {time.time()-tstart:.3f} seconds")

print(f"Script run time: {time.time()-tstart:.3f} seconds")

