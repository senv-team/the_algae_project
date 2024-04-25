import json
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt

SHP_FILE = '../../datasets/yang_shape_files/01.shp'
DBF_FILE = '../../datasets/yang_shape_files/01.dbf'
JSON_FILE = "mexico.geojson"

geodf = gpd.read_file(DBF_FILE)

geodf.plot()
plt.savefig("shape01.png")