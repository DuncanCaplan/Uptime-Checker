import threading
import time

import requests
from colorama import Fore, init
from flask import Flask
from prometheus_client import Gauge, generate_latest

url_up = Gauge("url_up", "Whether the URL is up (1) or down (0)", ["url"])
url_response_seconds = Gauge(
    "url_response_seconds", "Time taken for server to respond", ["url"]
)

app = Flask(__name__)

init(autoreset=True)


@app.route("/")
def home():
    return "OK"


@app.route("/health")
def health():
    return "Health"


@app.route("/metrics")
def metrics():
    return generate_latest()


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
                    url_up.labels(url=url).set(1)
                    url_response_seconds.labels(url=url).set(
                        response.elapsed.total_seconds()
                    )
                elif 300 <= response.status_code < 400:
                    print(Fore.YELLOW + f"URL {url} has been redirected.")
                    print(
                        Fore.CYAN
                        + f"Response time: {response.elapsed.total_seconds()} seconds."
                    )
                    url_up.labels(url=url).set(0)
                    url_response_seconds.labels(url=url).set(
                        response.elapsed.total_seconds()
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
                    url_up.labels(url=url).set(0)
                    url_response_seconds.labels(url=url).set(
                        response.elapsed.total_seconds()
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
                    url_up.labels(url=url).set(0)
                    url_response_seconds.labels(url=url).set(
                        response.elapsed.total_seconds()
                    )
            except requests.exceptions.RequestException as e:
                print(Fore.YELLOW + f"URL {url} is not reachable. Error: {e}")
                url_up.labels(url=url).set(0)
                url_response_seconds.labels(url=url).set(-1)

        time.sleep(30)


threading.Thread(target=check_all_urls).start()

if __name__ == "__main__":
    app.run(debug=True)
