import threading
import time

import requests
from colorama import Fore, init
from flask import Flask

app = Flask(__name__)

init(autoreset=True)


@app.route("/")
def home():
    return "OK"


@app.route("/health")
def health():
    return "Health"


def check_all_urls():
    file = open("urls.txt", "r")
    urls = file.readlines()
    file.close()

    while True:
        for url in urls:
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

        time.sleep(30)


threading.Thread(target=check_all_urls).start()

if __name__ == "__main__":
    app.run(debug=True)
