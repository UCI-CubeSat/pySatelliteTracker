import requests

BING_API_KEY = "AlG8wXq_mQ7kAhYeZzRQPsRPaFxei31_kBCmTW9P_RFOkhFBr1HCl9eT0NTkwEen"  # Insert API key here
BING_BASE_URL = "http://dev.virtualearth.net/REST/v1/Locations/US/{adminDistrict}/{postalCode}/{locality}/{" \
                "addressLine}?includeNeighborhood={includeNeighborhood}&include={includeValue}&maxResults={" \
                "maxResults}&key={BingMapsAPIKey}"


def getLatLong():
    # TODO
    # These variable should change base on front-end input
    country = "US"
    adminDistrict = "CA"
    postalCode = "92697"
    city = "Irvine"
    addressLine = "University%20of%20California,%20Irvine"
    # END of TODO
    returnFormat = "json"
    url = f'http://dev.virtualearth.net/REST/v1/Locations/' \
          f'{country}/{adminDistrict}/{postalCode}/{city}/{addressLine}?' \
          f'o={returnFormat}&key={BING_API_KEY}'
    response = requests.get(url).json()

    return response["resourceSets"][0]["resources"][0]["point"]["coordinates"], response
