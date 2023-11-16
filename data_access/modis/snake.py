import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# read the GeoJSON file
geojson_file = '../../datasets/modis/snake.geojson'  # replace with your GeoJSON file path
gdf = gpd.read_file(geojson_file)
# to zoom into the region covered by the GeoJSON file
x_min, y_min, x_max, y_max = gdf.total_bounds

# to get this data, go to https://oceancolor.gsfc.nasa.gov/l3/order/
# select monthly data, 4km resolution, and the mapped option
# then select the data and time range you want

# possible modes: 
modes = [
    { # 0
      "type": "chlor_a", 
      "filename": "../../datasets/modis/AQUA_MODIS.20230101_20230131.L3m.MO.CHL.chlor_a.4km.nc",
      "description": "Chlorophyll",
      "limits": [0, 1.5],
    },
    { # 1
      "type": "sst",
      "filename": "../../datasets/modis/AQUA_MODIS.20230101_20230131.L3m.MO.SST.sst.4km.nc",
      "description": "Sea Surface Temperature",
      "limits": [20, 40],
    },
    # { # 2
    #   "type": "poc",
    #   "filename": "../../datasets/modis/AQUA_MODIS.20230101.L3m.DAY.POC.poc.4km.nc",
    #   "description": "Particulate Organic Carbon"
    # }
]

my_data_cropped_list = []

for mode in modes:
  # read the data
  data = nc.Dataset(mode["filename"], "r")

  # read latitude, longitude and poc data
  latitude = data.variables['lat'][:]
  longitude = data.variables['lon'][:]
  my_data = data.variables[mode["type"]][:]

  # replace fill values with NaN for better plotting
  fill_value = data.variables[mode["type"]]._FillValue
  my_data = np.where(my_data == fill_value, np.nan, my_data)

  # set any data below 0 to np.nan
  my_data = np.where(my_data < 0, np.nan, my_data)

  my_data_cropped = my_data[(latitude >= y_min) & (latitude <= y_max), :]
  my_data_cropped = my_data_cropped[:, (longitude >= x_min) & (longitude <= x_max)]
  longitude_cropped = longitude[(longitude >= x_min) & (longitude <= x_max)]
  latitude_cropped = latitude[(latitude >= y_min) & (latitude <= y_max)]

  # plot data
  plt.figure(figsize=(12, 6))
  plt.pcolormesh(longitude, latitude, my_data)
  plt.colorbar(label=mode["description"])
  plt.xlabel('Longitude (degrees east)')
  plt.ylabel('Latitude (degrees north)')
  plt.xlim(x_min, x_max)
  plt.ylim(y_min, y_max)
  plt.clim(mode["limits"][0], mode["limits"][1])
  plt.title(f'MODISA Level-3 Standard Mapped Image for {mode["description"]}')
  plt.savefig(f'./{mode["type"]}.png')

  # append my_data_cropped to a list
  my_data_cropped_list.append(my_data_cropped)

# calculate the correlation coefficient between the two arrays in the list
# create a scatter plot of the data from the pixels in each array in the list
# remove NaN values from both arrays before calculating the correlation coefficient
not_nan_mask = ~np.isnan(my_data_cropped_list[0]) & ~np.isnan(my_data_cropped_list[1])
my_cc = np.corrcoef(my_data_cropped_list[0][not_nan_mask], my_data_cropped_list[1][not_nan_mask])[0, 1]

data1 = my_data_cropped_list[0][not_nan_mask]
data2 = my_data_cropped_list[1][not_nan_mask]
my_xcc = np.correlate(data1, data2)[0]
norm_xcc = my_xcc / np.sqrt(np.correlate(data1, data1)[0] * np.correlate(data2, data2)[0])

plt.figure(figsize=(12, 6))
plt.scatter(my_data_cropped_list[0][not_nan_mask], my_data_cropped_list[1][not_nan_mask])
plt.xlabel(modes[0]["description"])
plt.ylabel(modes[1]["description"])
plt.title(f'{modes[0]["description"]} vs {modes[1]["description"]}, r={my_cc:.2f}, xcc={norm_xcc:.2f}')
plt.savefig(f'./{modes[0]["type"]}_vs_{modes[1]["type"]}_cc.png')

## TO-DO
# add in the depth of the ocean at these points