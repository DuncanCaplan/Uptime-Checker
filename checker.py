import requests, colorama

from colorama import Fore


urls = open("urls.txt").readlines()

for line in urls:
    url = line.strip()
    try:
        response = requests.request("GET", url)

        if response.status_code != 200:
            print(Fore.RED + f"URL {url} is not reachable. Status code: {response.status_code}")
        else:
            print(f"URL {url} is reachable.")
            print(f"Response time: {response.elapsed.total_seconds()} seconds.")
    except requests.exceptions.RequestException as e:
        print(f"URL {url} is not reachable. Error: {e}")                   

