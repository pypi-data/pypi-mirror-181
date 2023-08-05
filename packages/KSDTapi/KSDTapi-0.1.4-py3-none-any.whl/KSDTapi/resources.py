import requests

def getResource(url):
    url_path = f"{url}/qcc/resources"

    response = requests.get(f"{url_path}") # , params=params)

    print("[Resource LIST] ", response.text, flush=True)

    return response.text