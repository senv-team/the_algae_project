import os
import sys
import warnings
from datetime import datetime

import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
from tqdm import tqdm

def geojson_context_figure(files: list[str]):
    ## plot the geojson regions over a world map for checking
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))  # type: ignore

    for file in files:
        gdf = gpd.read_file(file)  # load the region shape

        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        world.plot(ax=ax, color="lightgrey")
        gdf.plot(ax=ax, edgecolor="red", facecolor="none")
        ax.set_axis_off()
        output_path = file.replace(".geojson", ".png")
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()

dir = "../../datasets/yang_shape_files/"
files = [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith(".geojson")]

geojson_context_figure(files)