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


def get_proxies():
    proxies = []
    with open("proxies.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            proxies.append(row[0])
    return proxies

##beware proxies fail sometimes..only ones i found functional for free at least
# proxies = get_proxies()

#infinite loop around proxies
prox_gen = cycle(proxies)

#store all json data retrieved from api
all_data = []

##index from which the process starts
last_succesful_index = 0


## This process might TAKE A LOT on the basis of your patience and connection time...
## well you can always find better proxy list online
## if u find any bugs please let me know!

flag = True
for idx , row in df.iloc[last_succesful_index:].iterrows():
    x , y = row.values
    print("*"*50 + f"\n ITERATION={idx+1}| Fetching data for lat={x:.2f},lon={y:.2f}")
    #start by using proxies one-by-one until one succeeds
    ## we start by using proxy one
    failures = 0
    for proxy in prox_gen:
        print(f"Attempting sourcing with proxy {proxy}...")
        try:
            ##send HTTP request
            data = get_data(x , y , proxy)

            ##store data
            data.update({"lat":x,"lon":y})
            all_data.append(data)
            print("Dictionary has been updated!")

            ##break the infinite loop and continue to next (x,y)
            break
        except Exception as e:
            print(colored(f"PROXY {proxy} FAILED! Error: {e}","red"))
            ##counting failed attempts
            failures += 1
            print(f"TOTAL FAILURES={failures}!")

            ##if we tried all proxies and none succeeded break loop
            ##and terminate
            if failures == len(proxies):
                flag = False
                break
            ##else retry with another proxy
            else:
                print("RETRYING...")
                continue

    ##all proxies failed = terminate procedure
    if not flag:
        ##before terminating store the last index on which the process
        ##was succesful to start from there
        last_succesful_index = idx - 1
        print(f"Last succesful index: {last_succesful_index}")
        break
