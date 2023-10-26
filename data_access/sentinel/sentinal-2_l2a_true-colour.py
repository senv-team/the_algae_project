import os
from sentinelhub import WmsRequest, BBox, CRS, DataCollection, SHConfig
import geopandas as gpd
import matplotlib.pyplot as plt

### ADD CREDENTIALS HERE ###

# set up configuration
config = SHConfig()
config.sh_client_id = my_client_id
config.sh_client_secret = my_client_secret
config.instance_id = my_instance_id

# load the geojson file into a geodataframe
gdf = gpd.read_file("map.geojson")

# print the crs
print(gdf.crs)

# find bounding box
bbox_coords = gdf.total_bounds  # it returns [minx, miny, maxx, maxy]
bbox_coords = [bbox_coords[0], bbox_coords[1], bbox_coords[2], bbox_coords[3]]  # reordering to [miny, minx, maxy, maxx]

# create a BBox object
bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)

# initiate WMS request
l2a_request = WmsRequest(
    data_collection=DataCollection.SENTINEL2_L2A,
    layer="TRUE-COLOR-S2-L2A",
    bbox=bbox,
    # time="2017-07-30",
    time=("2017-08-01", "2017-08-31"),
    width=2048,
    config=config
)

# fetch data
l2a_data = l2a_request.get_data()

# plot and save image
def plot_image(image):
    plt.imshow(image)
    plt.axis('off')
    plt.savefig('out.png', bbox_inches='tight',dpi=2000)

plot_image(l2a_data[0])