import requests, sys, concurrent.futures

from colorama import Fore, init

init(autoreset=True)


def check_url(url):
    url = url.strip()

    try:
        response = requests.request("GET", url)

        if 200 <= response.status_code < 300:
            print(
                Fore.GREEN
                + f"URL {url} is reachable. Status code: {response.status_code}"
            )
            print(
                Fore.CYAN
                + f"Response time: {response.elapsed.total_seconds()} seconds."
            )
        elif 300 <= response.status_code < 400:
            print(Fore.YELLOW + f"URL {url} has been redirected.")
            print(
                Fore.CYAN
                + f"Response time: {response.elapsed.total_seconds()} seconds."
            )
        elif 400 <= response.status_code < 500:
            print(
                Fore.RED
                + f"URL {url} returned a client error status code: {response.status_code}"
            )
            print(
                Fore.CYAN
                + f"Response time: {response.elapsed.total_seconds()} seconds."
            )
        elif 500 <= response.status_code < 600:
            print(
                Fore.RED
                + f"URL {url} returned a server error status code: {response.status_code}"
            )
            print(
                Fore.CYAN
                + f"Response time: {response.elapsed.total_seconds()} seconds."
            )
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"URL {url} is not reachable. Error: {e}")


with open(sys.argv[1], "r") as urls_file:

    urls = urls_file.readlines()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(check_url, urls)
