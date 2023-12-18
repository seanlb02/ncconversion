


import xarray as xr 
import rioxarray as rio 
import numpy 
import rasterio
import subprocess

# Easily open NC files and store as xarrays - so they can be easily manipulated:
nc_file = xr.open_dataset('C:/Users/SeanGyuris/Downloads/rain_2033.nc')

# Be able to visualise the underlying data to simplify manipulation
print(nc_file['pr-fl'])

# Parameters with xarray is calculable...
# E.g Daily Precipitation can be annualised or averaged:
summation = sum(nc_file['pr-fl'])

# Assign and reset CRS projections:
xarr = summation.rio.set_spatial_dims(x_dim='lon', y_dim='lat')
xarr.rio.write_crs("epsg:4326", inplace=True)

# CRS is QA'd:
print(xarr.rio.crs)

# identify and remove any attributes that may complicate conversion to TIFF:
print(xarr.attrs)
del xarr.attrs['grid_mapping']

# transform the NetCDF4 file to .tiff and store locally:
xarr.rio.to_raster(r"C:/Users/SeanGyuris/Downloads/prec_2033_year_test.tiff")

# Simple to store the transformed raster within local or remote database instance as the client needs:
# cmds = 'raster2pgsql -I -C -e -Y -F -s [EPSG] -t 250x250 -l 2,4 [image_name].tiff [schema].[table] | psql -U postgres -d gisdb -h localhost -p 5432'
# subprocess.call(cmds, shell=True)
