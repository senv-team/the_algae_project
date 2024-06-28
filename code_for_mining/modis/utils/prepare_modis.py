import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

# overriding requests.Session.rebuild_auth to maintain headers when redirected
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = "urs.earthdata.nasa.gov"

    def __init__(self, username: str, password: str):
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


def download_data(urls: list[str], output_directory: str, username: str, password: str):
    session = SessionWithHeaderRedirection(username, password)

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    for url in urls:
        filename = os.path.join(output_directory, url[url.rfind("/") + 1 :])

        try:
            response = session.get(url, stream=True)
            logging.info(f"Downloading {url}, status code: {response.status_code}")
            response.raise_for_status()

            with open(filename, "wb") as fd:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    fd.write(chunk)

            logging.info(f"Downloaded {url} to {filename}")

        except requests.exceptions.HTTPError as e:
            logging.error(f"Error downloading {url}: {e}")





