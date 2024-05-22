import json
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
import os

# directories
MAIN_DIR = '../../datasets/yang_shape_files/'
SHP_FILE_DIR = MAIN_DIR
JSON_FILE_DIR = MAIN_DIR

shp_files = [os.path.join(SHP_FILE_DIR, f) for f in os.listdir(SHP_FILE_DIR) if f.endswith('.shp')]

for shp_file in shp_files:
    gdf = gpd.read_file(shp_file)
    output_file = shp_file.replace('.shp', '.geojson')
    gdf.to_file(output_file, driver='GeoJSON')
    print(f"Saved {output_file}")