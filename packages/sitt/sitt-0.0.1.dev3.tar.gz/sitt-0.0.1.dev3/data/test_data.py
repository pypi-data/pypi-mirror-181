#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netCDF4 import Dataset, date2index
import numpy as np
import datetime as dt

rootgrp = Dataset("era5_data_2m_temperature.nc", "r", format="NETCDF4")

lat, lon = rootgrp.variables['latitude'][:], rootgrp.variables['longitude'][:]
times = rootgrp.variables['time']

in_lat = 46.61360133
in_lon = 13.84586334
in_date = dt.datetime.fromisoformat('1995-07-01 14:00')

# get index of time
time_idx = date2index(in_date, times, select='nearest')

# get index of lat/lon
lat_idx = (np.abs(lat - in_lat)).argmin()
lon_idx = (np.abs(lon - in_lon)).argmin()

temp = rootgrp.variables['t2m']

print(temp[time_idx][lat_idx][lon_idx] - 273.15)
