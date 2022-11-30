#Imports:
import requests
import pandas as pd
import numpy as np
import csv
from termcolor import colored
from itertools import cycle
import time

# proxy = pd.read_csv('proxies/proxies.csv')

##http request to api
##change timeout if u do not want to wait for the proxy a lot
def get_data(lat, lon, proxy , timeout = 5):
    url = f"https://apps.solargis.com/api/data/lta?loc={lat},{lon}"
    requests.request.headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    response = requests.request("GET",
                                url,
                                proxies={
                                    "http": proxy,
                                    "https": proxy
                                },
                                timeout=timeout)
    if response.status_code == 200:
        return response.json().get("annual").get("data")

    ##returns none if request wasn't succesful
    return
