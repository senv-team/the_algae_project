import glob
import logging
import os

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import netCDF4 as nc

# Set up logging
logging.basicConfig(level=logging.INFO)


def plot_poc_data(file_paths: list[str]):
    # Get list of all .nc files
    #files = glob.glob(file_path + "*.nc")

    for file in file_paths:
        try:
            # Load the netCDF file
            data = nc.Dataset(file)
            date = data.date_created[:10]
            # Extract poc data as a numpy array
            poc = data["poc"][:]

            # Create a GeoAxes with plate carree projection
            ax = plt.axes(projection=ccrs.PlateCarree())

            # Add land, coastlines and gridlines
            ax.add_feature(cfeature.LAND)
            ax.coastlines()
            ax.gridlines()

            # Plot the poc data as a pcolormesh
            plt.pcolormesh(
                data["lon"][:], data["lat"][:], poc, transform=ccrs.PlateCarree()
            )

            plt.title(f"Particulate Organic Carbon {date}")
            # Add axis labels
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")

            # Add colorbar
            cbar = plt.colorbar()
            cbar.set_label("Particulate Organic Carbon (mg/m^3)")

            # Set colorbar tick locations and labels
            cbar.set_ticks([0, 200, 400, 600, 800])
            cbar.set_ticklabels(["0", "200", "400", "600", "800"])

            # Show the plot
            plt.show()

        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")


def save_netcdf_info_to_text(file_paths: list[str]) -> None:
    """Saves information from multiple NetCDF files to text files.

    Args:
        file_paths: A list of paths to the NetCDF files.
    """

    os.makedirs("nc_files", exist_ok=True)  # Create the directory if it doesn't exist

    for file_path in file_paths:
        try:
            with nc.Dataset(file_path) as ds:
                text_file_path = f"nc_files/{os.path.basename(file_path)}_info.txt"

                with open(text_file_path, "w") as text_file:
                    print("Dataset Information:", file=text_file)
                    print(ds, file=text_file)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def count_empty_netcdf_files(file_paths: list[str]) -> int:
    """Counts the number of empty NetCDF files in a given list of file paths.

    Args:
        file_paths: A list of paths to the NetCDF files.

    Returns:
        The number of empty files found.
    """

    empty_count = 0
    for file_path in file_paths:
        try:
            with nc.Dataset(file_path, "r") as ds:
                variables = ds.variables
                if not variables:  # Check for empty variables directly
                    empty_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return empty_count


import netCDF4 as nc

def count_empty_netcdf_files(file_paths: list[str]) -> tuple[int, list[str]]:
    """Counts empty NetCDF files and categorizes files based on empty variables.

    Args:
        file_paths: A list of paths to the NetCDF files.

    Returns:
        A tuple containing:
        - The number of empty files found.
        - A list of file paths with variables.
    """

    empty_count = 0
    #empty_files = []
    non_empty_files: list[str] = []

    for file_path in file_paths:
        try:
            with nc.Dataset(file_path, "r") as ds:
                variables = ds.variables
                if not variables:
                    empty_count += 1
                    #empty_files.append(file_path)
                else:
                    non_empty_files.append(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return empty_count, non_empty_files

