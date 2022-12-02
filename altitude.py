import requests

def altitude(latitude, longitude):
    BASE_URI ="https://api.opentopodata.org/v1/test-dataset?locations="

    # Given a latitude and a longitude, the altitude will be calculate it

    url = BASE_URI+str(latitude)+","+ str(longitude)

    altitude = requests.get(url).json()
    return altitude["results"][0]
