import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# read the data
filename = "./AQUA_MODIS.20230101_20230131.L3m.MO.CHL.chlor_a.4km.nc"
data = nc.Dataset(filename, "r")

print("=== GLOBAL ATTRIBUTES ===")
for attr in data.ncattrs():
    print(f"{attr}: {data.getncattr(attr)}")

print("\n=== DIMENSIONS ===")
for dim, dim_info in data.dimensions.items():
    print(f"{dim}: {len(dim_info)}")

print("\n=== VARIABLES ===")
for var, var_info in data.variables.items():
    print(f"{var}: {var_info}")

print("\n=== GROUPS ===")
for group in data.groups:
    print(group)

###################

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# read latitude, longitude and poc data
latitude = data.variables['lat'][:]
longitude = data.variables['lon'][:]
poc_data = data.variables['chlor_a'][:]

# replace fill values with NaN for better plotting
fill_value = data.variables['chlor_a']._FillValue
poc_data = np.where(poc_data == fill_value, np.nan, poc_data)

# # apply the scale_factor and add_offset
# scale_factor = data.variables['chlor_a'].scale_factor
# add_offset = data.variables['chlor_a'].add_offset
# poc_data = poc_data * scale_factor + add_offset

# plot data
plt.figure(figsize=(12, 6))
plt.pcolormesh(longitude, latitude, poc_data)
plt.colorbar(label='Chlorophyll-a (mg m^-3)(?)')
plt.xlabel('Longitude (degrees east)')
plt.ylabel('Latitude (degrees north)')
plt.title('MODISA Level-3 Standard Mapped Image for Chlorophyll-a')
plt.savefig('modis_chl.png')
plt.close()

import geopandas as gpd

# read and plot the GeoJSON file
geojson_file = 'map.geojson'  # replace with your GeoJSON file path
gdf = gpd.read_file(geojson_file)

for polygon in gdf.geometry:
  x,y = polygon.exterior.xy
  plt.plot(x, y, color="red")  # adjust the color as you like

# to zoom into the region covered by the GeoJSON file
x_min, y_min, x_max, y_max = gdf.total_bounds

# set any data below 0 to np.nan
my_poc_data = np.where(poc_data < 0, np.nan, poc_data)

# print the max and min values of my_poc_data
print(np.nanmax(my_poc_data))
print('----')
print(np.nanmin(my_poc_data))

# find the maximum and minimum values of the data between the range of 6000 and 8000
min_value = 0
max_value = 20

# plot data
plt.figure(figsize=(12, 6))
plt.pcolormesh(longitude, latitude, poc_data)
plt.colorbar(label='Particulate Organic Carbon (mg m^-3)')
plt.xlabel('Longitude (degrees east)')
plt.ylabel('Latitude (degrees north)')
plt.title('MODISA Level-3 Standard Mapped Image for Chlorophyll-a')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.clim(min_value, max_value)
plt.savefig('modis_chl_crop.png')
plt.close()

# plot a histogram of the data excluding values below 1000
plt.figure(figsize=(12, 6))
plt.hist(poc_data[~np.isnan(poc_data)], bins=100, range=(0, 87))
plt.xlabel('Particulate Organic Carbon (mg m^-3)')
plt.ylabel('Frequency')
plt.title('Histogram of chlorophyll-a data')
plt.savefig('modis_chl_hist.png')
plt.close()