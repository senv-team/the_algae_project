import os
import requests
from tqdm import tqdm
import os

class SessionWithHeaderRedirection(requests.Session):
  AUTH_HOST = "urs.earthdata.nasa.gov"
  def __init__(self, username, password):
    super().__init__()
    self.auth = (username, password)
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

# define the path to the text file containing the URLs
url_file = "urls.txt"

# read the URLs from the text file
with open(url_file, "r") as file:
  urls = file.read().splitlines()

# create session with the user credentials that will be used to authenticate access to the data
username = "senv_team"
password = "ketchup&Mustard1"
session = SessionWithHeaderRedirection(username, password)

# download the files
for url in tqdm(urls):
  # extract the filename from the URL
  filename = url.split("/")[-1]
  
  # build the path to save the downloaded file
  save_path = os.path.join('./', filename)

  # check if the file already exists
  if not os.path.exists(save_path):
  
    try:
      response = session.get(url, stream=True)
      print(f"status code: {response.status_code}")
      response.raise_for_status()

      # save the file
      with open(filename, "wb") as fd:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
          # print(chunk)

          fd.write(chunk)

    except requests.exceptions.HTTPError as e:
      print(f"HTTP error occurred: {e}")