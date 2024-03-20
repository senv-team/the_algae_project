import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from datetime import datetime
from tqdm import tqdm
import sys

## import the GeoJSON files which contains the coordinates of the region(s) of interest

locs_dir = "/gpfs/data/fs70652/jamesm/senv/the_algae_project/data_process/correlation/locs"
locs_files = [os.path.join(locs_dir, file) for file in os.listdir(locs_dir) if
                  file.endswith(".geojson")] # find all the geojson files in a directory

gdf_list = [gpd.read_file(locs_file) for locs_file in locs_files] # read the GeoJSON files

x_min_list = [gdf.total_bounds[0] for gdf in gdf_list] # set the limits of the region(s) of interest with lists for each min and max
y_min_list = [gdf.total_bounds[1] for gdf in gdf_list]
x_max_list = [gdf.total_bounds[2] for gdf in gdf_list]
y_max_list = [gdf.total_bounds[3] for gdf in gdf_list]

## import the data files
data_dir = "/gpfs/data/fs70652/jamesm/senv/the_algae_project/datasets/modis"
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".nc")]
data_files.sort() # sort the list of files alphabetically
start_date = [datetime.strptime(file.split("/")[-1].split(".")[1].split("_")[0], "%Y%m%d") for file in data_files] # parse the start and end date information from the filename (AQUA_MODIS.20210101_20210131.L3m.MO.CHL.chlor_a.4km.nc) of each file and convert it to a datetime object
end_date = [datetime.strptime(file.split("/")[-1].split(".")[1].split("_")[1], "%Y%m%d") for file in data_files]
data_files_info = [{"filename": file, "start_date": start, "end_date": end} for file, start, end in zip(data_files, start_date, end_date)] # create a list of dictionaries containing the filename, start date and end date for each file
start_date_range = datetime(2021, 1, 1) # specify the start and end dates for the desired date range
end_date_range = datetime(2022, 12, 31)

print(f'Total data files available: {len(data_files_info)}') # print the the number of data files available

filtered_files_info = [file_info for file_info in data_files_info if start_date_range <= file_info["start_date"] <= end_date_range and start_date_range <= file_info["end_date"] <= end_date_range] # filter the data_files_info list based on the date range

print(f'Selected date range: {start_date_range} to {end_date_range}') # print the number of data files available within the date range
print(f'Total data files available within the date range: {len(filtered_files_info)}') # print the number of data files available within the date range

successful_loads = 0
unsuccessful_loads = 0
data_list = []

for file_info in tqdm(filtered_files_info, desc='Loading global data'): # read the data
  try:
    data = nc.Dataset(file_info["filename"], "r")
    successful_loads += 1
    data_list.append({"data": data, "start_date": file_info["start_date"], "end_date": file_info["end_date"]})
  except:
    unsuccessful_loads += 1

print(f"Successful loads: {successful_loads}") # print the number of successful and unsuccessful loads
print(f"Unsuccessful loads: {unsuccessful_loads}")
print(f"Size of data loaded: {sys.getsizeof(data_list)} bytes (~{(sys.getsizeof(data_list) / 1024**3):.2f} GB)")

# go through the data list, and for each item, crop the data to the region of interest
data_crop_list = []

for data_info in tqdm(data_list, desc='Cropping data to region of interest'): # loop through all the data, and crop it to the region of interest
  latitude = data_info["data"]["lat"][:] # read latitude and longitude data
  longitude = data_info["data"]["lon"][:]
  chlor_a = data_info["data"]["chlor_a"][:] # read the chlorophyll data
  fill_value = data_info["data"]["chlor_a"]._FillValue # replace fill values with NaN for better plotting
  chlor_a[chlor_a == fill_value] = np.nan
  chlor_a[chlor_a < 0] = np.nan # set any data below 0 to NaN
  chlor_a_crop = chlor_a[(latitude >= y_min_list[0]) & (latitude <= y_max_list[0]), :] # crop the data to the region of interest
  chlor_a_crop = chlor_a_crop[:, (longitude >= x_min_list[0]) & (longitude <= x_max_list[0])]
  longitude_crop = longitude[(longitude >= x_min_list[0]) & (longitude <= x_max_list[0])]
  latitude_crop = latitude[(latitude >= y_min_list[0]) & (latitude <= y_max_list[0])]
  data_crop_list.append({"data": chlor_a_crop, "latitude": latitude_crop, "longitude": longitude_crop, "start_date": data_info["start_date"], "end_date": data_info["end_date"]})

del data_list # remove the data_list from memory
print('Data cropped.')
print(f'New size of data: {sys.getsizeof(data_crop_list)} bytes (~{(sys.getsizeof(data_crop_list) / 1024**3):.2f} GB)')