import requests
import pandas as pd

base_url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/'

headers = {
    'token': 'UNpWhKdEkCqBoPyQftGcteuVEsyHkikK' # access token (https://www.ncdc.noaa.gov/cdo-web/webservices/v2)
}

def get_data(endpoint, params=None):
    """
    Generic function to fetch data from the CDO API.
    :param endpoint: API endpoint (e.g., 'datasets', 'datacategories').
    :param params: Optional dictionary containing URL parameters.
    :return: JSON response from the API.
    """

    url = base_url + endpoint # construct the full URL

    response = requests.get(url, headers=headers, params=params) # make the request
    
    if response.status_code == 200: # check if the request was successful
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

if __name__ == "__main__":

    params = { # enter search parameters (e.g. https://realworlddatascience.net/ideas/tutorials/posts/2023/04/13/flowers.html#:~:text=1839%20and%201852.-,year,-date)
        'datasetid': 'GHCND',
        'stationid': 'GHCND:BE000006447',
        'startdate': '1839-01-01',
        'enddate': '1839-01-10'
    }

    daily_data = get_data('data', params=params) # fetch data

    if daily_data: # check if we received data

        results = daily_data.get('results', []) # extract results if any

        data_dict = {} # dictionary to hold data

        for record in results: # populate the dictionary with new rows
            date = record['date']
            if date not in data_dict:
                data_dict[date] = {'date': date, 'TMAX': None, 'TMIN': None, 'TAVG': None}
            if record['datatype'] == 'TMAX':
                data_dict[date]['TMAX'] = record['value']/10
            elif record['datatype'] == 'TMIN':
                data_dict[date]['TMIN'] = record['value']/10

        for date in data_dict: # calculate average temperature
            if data_dict[date]['TMAX'] and data_dict[date]['TMIN']:
                data_dict[date]['TAVG'] = (data_dict[date]['TMAX'] + data_dict[date]['TMIN']) / 2

        df = pd.DataFrame(data_dict.values()) # convert dictionary to DataFrame
        
        print(df)