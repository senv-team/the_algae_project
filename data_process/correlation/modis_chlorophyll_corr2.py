import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from datetime import datetime
from tqdm import tqdm
import sys
import pandas as pd

def geojson_context_fig(files):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    for locs_file in locs_files:
        gdf = gpd.read_file(locs_file)
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        world.plot(ax=ax, color='lightgrey')
        gdf.plot(ax=ax, edgecolor='red', facecolor="none")
        ax.set_axis_off()
        output_path = locs_file.replace('.geojson', '.png')
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()

    return True

def plot_data(region_name, data, latitude, longitude, start_date, end_date):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect('equal')
    plt.pcolormesh(longitude, latitude, data, shading='auto', vmin=0, vmax=0.75)
    plt.colorbar(label='Chlorophyll-a concentration', extend='max')
    plt.title(f"Region: {region_name}\n{start_date} to {end_date}")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(f"./plots/{region_name}/{start_date}_{end_date}.png")
    plt.close()

def plot_time_series(data_series, region_name):
    dates = [info['start_date'] for info in data_series]
    # Ensure that the data is copied from the original dataset to a writable array
    means = [np.nanmean(np.array(info['data'])) for info in data_series if info['data'].size > 0]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, means, marker='o', linestyle='-')
    plt.title(f"Time Series of Mean Chlorophyll-a Concentration for {region_name}")
    plt.xlabel('Date')
    plt.ylabel('Mean Chlorophyll-a Concentration')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"./plots/{region_name}/time_series.png")
    plt.close()

def write_to_csv(data_series, region_name):
    try:
        valid_data_series = [d for d in data_series if 'start_date' in d and 'end_date' in d and d['data'].size > 0]

        if not valid_data_series:
            print(f"No valid data to process for {region_name}.")
            return

        # Define columns as just the months in a single year
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Create an empty DataFrame with years as index and months as columns
        years = sorted(set([d['start_date'].year for d in valid_data_series]))
        df = pd.DataFrame(index=years, columns=months)

        for entry in valid_data_series:
            data_copy = np.array(entry['data']).copy()
            mean_value = np.nanmean(data_copy) if np.any(~np.isnan(data_copy)) else np.nan
            month = entry['start_date'].strftime('%b')
            year = entry['start_date'].year
            # Set the mean value at the correct year and month
            df.at[year, month] = mean_value

        # Remove any rows that are entirely NaN
        df.dropna(how='all', inplace=True)

        # Ensure directory exists
        os.makedirs(f"./data_csv/{region_name}", exist_ok=True)

        # Save to CSV
        csv_path = f"./data_csv/{region_name}/chlorophyll_monthly_means_{region_name}.csv"
        df.to_csv(csv_path)
        print(f"CSV file created for {region_name} at {csv_path}")
    except Exception as e:
        print(f"Failed to process data for {region_name}. Error: {e}")

locs_dir = "../../datasets/yang_shape_files"
locs_files = [os.path.join(locs_dir, file) for file in os.listdir(locs_dir) if file.endswith(".geojson")]
istat = geojson_context_fig(locs_files)
gdf_list = [gpd.read_file(locs_file) for locs_file in locs_files]

# Calculate bounding boxes for each region
y_min_list = [gdf.total_bounds[1] for gdf in gdf_list]
y_max_list = [gdf.total_bounds[3] for gdf in gdf_list]
x_min_list = [gdf.total_bounds[0] for gdf in gdf_list]
x_max_list = [gdf.total_bounds[2] for gdf in gdf_list]

data_dir = "../../datasets/modis"
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".nc")]
data_files.sort()
start_date = [datetime.strptime(file.split("/")[-1].split(".")[1].split("_")[0], "%Y%m%d") for file in data_files]
end_date = [datetime.strptime(file.split("/")[-1].split(".")[1].split("_")[1], "%Y%m%d") for file in data_files]
data_files_info = [{"filename": file, "start_date": start, "end_date": end} for file, start, end in zip(data_files, start_date, end_date)]
start_date_range = datetime(2000, 1, 1)
end_date_range = datetime(2005, 1, 1)

filtered_files_info = [file_info for file_info in data_files_info if start_date_range <= file_info["start_date"] <= end_date_range and start_date_range <= file_info["end_date"] <= end_date_range]
successful_loads = 0
unsuccessful_loads = 0
data_list = []

for file_info in tqdm(filtered_files_info, desc='Loading global data'):
    try:
        data = nc.Dataset(file_info["filename"], "r")
        successful_loads += 1
        data_list.append({"data": data, "start_date": file_info["start_date"], "end_date": file_info["end_date"]})
    except:
        unsuccessful_loads += 1

time_series_data = {gdf_name: [] for gdf_name in [os.path.basename(locs_file).replace('.geojson', '') for locs_file in locs_files]}

for data_info in tqdm(data_list, desc='Cropping data to region of interest'):
    latitude = data_info["data"]["lat"][:]
    longitude = data_info["data"]["lon"][:]
    chlor_a = data_info["data"]["chlor_a"][:]
    fill_value = data_info["data"]["chlor_a"]._FillValue
    chlor_a[chlor_a == fill_value] = np.nan
    chlor_a[chlor_a < 0] = np.nan

    for i, gdf in enumerate(gdf_list):
        chlor_a_crop = chlor_a[(latitude >= y_min_list[i]) & (latitude <= y_max_list[i]), :]
        chlor_a_crop = chlor_a_crop[:, (longitude >= x_min_list[i]) & (longitude <= x_max_list[i])]
        longitude_crop = longitude[(longitude >= x_min_list[i]) & (longitude <= x_max_list[i])]
        latitude_crop = latitude[(latitude >= y_min_list[i]) & (latitude <= y_max_list[i])]
        region_name = os.path.basename(locs_files[i]).replace('.geojson', '')
        time_series_data[region_name].append({"data": chlor_a_crop, "start_date": data_info["start_date"], "end_date": data_info["end_date"]})

for region_name, data_series in time_series_data.items():

    os.makedirs(f"./plots/{region_name}", exist_ok=True)
    # plot_time_series(data_series, region_name)
    write_to_csv(data_series, region_name)

del data_list
print('Data cropped and time series plotted.')