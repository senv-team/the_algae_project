#!/usr/bin/python

# https://urs.earthdata.nasa.gov/documentation/for_users/data_access/python

import requests  # get the requsts library from https://github.com/requests/requests
import os

# Open the file in read mode
with open("urls.txt", "r") as f:
    # Read all lines into a list
    urls = f.readlines()

urls = [url.strip() for url in urls]


# overriding requests.Session.rebuild_auth to mantain headers when redirected
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = "urs.earthdata.nasa.gov"

    def __init__(self, username, password):
        super().__init__()

        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from

    # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers

        url = prepared_request.url

        if "Authorization" in headers:
            original_parsed = requests.utils.urlparse(response.request.url)

            redirect_parsed = requests.utils.urlparse(url)

            if (
                (original_parsed.hostname != redirect_parsed.hostname)
                and redirect_parsed.hostname != self.AUTH_HOST
                and original_parsed.hostname != self.AUTH_HOST
            ):
                del headers["Authorization"]

        return


# create session with the user credentials that will be used to authenticate access to the data

username = "senv_team"
password = "ketchup&Mustard1"
session = SessionWithHeaderRedirection(username, password)


# the url of the file we wish to retrieve

# url = "https://n5eil01u.ecs.nsidc.org/MOST/MOD10A1.006/2016.12.31/MOD10A1.A2016366.h14v03.006.2017002110336.hdf.xml"
# url = "https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2023/0914/AQUA_MODIS.20230914.L3m.DAY.CHL.chlor_a.4km.NRT.nc.png"
# url = "https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2023/0913/AQUA_MODIS.20230913.L3m.DAY.CHL.chlor_a.4km.NRT.nc.png"

# urls = [
#     "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/AQUA_MODIS.20230101.L3m.DAY.POC.poc.4km.nc",
#     "https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/POC/L3/2023/0101/AQUA_MODIS.20230101.L3m.DAY.POC.poc.4km.nc.png",
#     "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/AQUA_MODIS.20230101.L3b.DAY.POC.NRT.nc",
# ]
# extract the filename from the url to be used when saving the file


if not os.path.isdir("tmp_dir"):
    os.makedirs("tmp_dir")

for url in urls:
    filename = os.path.join("tmp_dir", url[url.rfind("/") + 1 :])

    try:
        # submit the request using the session

        response = session.get(url, stream=True)

        print(f"status code: {response.status_code}")

        # raise an exception in case of http errors
        response.raise_for_status()

        # save the file
        with open(filename, "wb") as fd:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                # print(chunk)

                fd.write(chunk)

    except requests.exceptions.HTTPError as e:
        # handle any errors here

        print(e)
