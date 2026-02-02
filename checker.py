import requests

urls = open("urls.txt").readlines()

for line in urls:
    url = line.strip()
    try:
        response = requests.request("GET", url)

        if response.status_code != 200:
            print(f"URL {url} is not reachable. Status code: {response.status_code}")
        else:
            print(f"URL {url} is reachable.")
    except requests.exceptions.RequestException as e:
        print(f"URL {url} is not reachable. Error: {e}")                   

