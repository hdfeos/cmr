"""
Copyright (C) 2017 The HDF Group

This example code illustrates how to access and visualize a GESDISC AIRS swath
in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python AIRH2RET.py

The HDF file must be searchable by CMR and served by OPeNDAP server.

Tested under: Python 2.7.10 :: Anaconda 2.3.0 (x86_64)
Last updated: 2017-1-05
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pyCMR import CMR
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset    

cmr=CMR("cmr.cfg")

# Here are sample CMR usages.
#
# results = cmr.searchCollection(platform='AQUA',provider='GES_DISC')
# results = cmr.searchGranule(limit=1000,short_name="MOD09CMG",temporal="2010-02-01T10:00:00Z,2010-02-01T12:00:00Z")

# MLS granule search doesn't return OPeNDAP URL.
# results = cmr.searchGranule(limit=2,short_name="ML2BRO")

# AIRS granule search doesn't return OPeNDAP URL.
# Retrieve the latest dataset using sort key.
results_g = cmr.searchGranule(limit=1,short_name="AIRH2RET",sort_key='-start_date')

# Collection does but it doesn't have <Type>OPeNDAP</Type> like GHRC result.
results = cmr.searchCollection(limit=1,short_name="AIRH2RET")

# This one returns OPeNDAP URL that has <Type>OPeNDAP</Type>
# but the URL doesn't return granule level URL.
#
# For example, it returns directory that has the granule unerneath:
# http://ghrc.nsstc.nasa.gov/opendap/ssmi/f14/monthly/
#
# results = cmr.searchGranule(concept_id='G550016-GHRC')

print len(results)
for res in results:
    # Check OPeNDAP URL.
    print  res.getOPeNDAPUrl()    

print len(results_g)
ourl = ''
for res in results_g:
    print res.getDownloadUrl()
    ourl = res.getDownloadUrl()

# For GES_DISC, the download URL matches OPeNDAP URL except
# '/data/' and '/opendap/'.
FILE_NAME = ourl.replace("data", "opendap")
print FILE_NAME

DATAFIELD_NAME = 'topog'
nc = Dataset(FILE_NAME)
data = nc.variables[DATAFIELD_NAME][:,:]
latitude = nc.variables['Latitude'][:]
longitude = nc.variables['Longitude'][:]

# Replace the filled value with NaN, replace with a masked array.
data[data == -9999.0] = np.nan
datam = np.ma.masked_array(data, np.isnan(data))
    
# Draw a polar stereographic projection using the low resolution coastline
# database.
m = Basemap(projection='npstere', resolution='l',
            boundinglat=30, lon_0 = 180)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(-80., -50., 5.))
m.drawmeridians(np.arange(-180., 181., 20.), labels=[1, 0, 0, 1])
x, y = m(longitude, latitude)
m.pcolormesh(x, y, datam)

# See page 101 of "AIRS Version 5.0 Released Files Description" document 
# [1]for unit specification.
units = 'm'
cb = m.colorbar()
cb.set_label('Unit:'+units)
    
basename = os.path.basename(FILE_NAME)
plt.title('{0}\n {1}'.format(basename, DATAFIELD_NAME))
fig = plt.gcf()
# plt.show()
pngfile = "{0}.py.png".format(basename)
fig.savefig(pngfile)

