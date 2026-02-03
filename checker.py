import requests, colorama, sys

from colorama import Fore, init

init(autoreset=True)

urls = open(sys.argv[1]).readlines()

for line in urls:
    url = line.strip()
    try:
        response = requests.request("GET", url)

        if response.status_code != 200:
            print(Fore.RED + f"URL {url} is not reachable. Status code: {response.status_code}")
        else:
            print(Fore.GREEN + f"URL {url} is reachable.")
            print(Fore.CYAN + f"Response time: {response.elapsed.total_seconds()} seconds.")
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"URL {url} is not reachable. Error: {e}")                   

