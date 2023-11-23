import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from datetime import datetime

# read the GeoJSON file
geojson_file = '../../datasets/modis/snake.geojson'  # replace with your GeoJSON file path
gdf = gpd.read_file(geojson_file)
# to zoom into the region covered by the GeoJSON file
x_min, y_min, x_max, y_max = gdf.total_bounds

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

# get a list of all the files a directory which has all the data files
data_dir = "/gpfs/data/fs70652/jamesm/senv/the_algae_project/datasets/modis"
# create a list of all the .nc files in the directory
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".nc")]
# sort the list of files alphabetically
data_files.sort()
# parse the start and end date information from the filename (AQUA_MODIS.20210101_20210131.L3m.MO.CHL.chlor_a.4km.nc) of each file
# and convert it to a datetime object
start_date = [datetime.strptime(file.split("/")[-1].split(".")[1].split("_")[0], "%Y%m%d") for file in data_files]
end_date = [datetime.strptime(file.split("/")[-1].split(".")[1].split("_")[1], "%Y%m%d") for file in data_files]

# create a list of dictionaries containing the filename, start date and end date for each file
data_files_info = [{"filename": file, "start_date": start, "end_date": end} for file, start, end in zip(data_files, start_date, end_date)]


# specify the start and end dates for the desired date range
start_date_range = datetime(2021, 1, 1)
end_date_range = datetime(2022, 12, 31)

# filter the data_files_info list based on the date range
filtered_files_info = [file_info for file_info in data_files_info if start_date_range <= file_info["start_date"] <= end_date_range and start_date_range <= file_info["end_date"] <= end_date_range]

print(filtered_files_info)

# # loop through the filtered list of files
# for file_info in filtered_files_info:
#   # read the data
#   data = nc.Dataset(file_info["filename"], "r")

#   # rest of the code...
#   # ...

import sys;sys.exit()

# rest of the code...
# ...
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