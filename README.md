# Uptime-Checker

A web service that continuously monitors a list of URLs and exposes the results as Prometheus metrics.

## How to run locally
```
python3 checker.py
```

## How to run with Docker

Build the image:
```
docker build -t uptime-checker .
```

Run the container:
```
docker run uptime-checker
```

Mount a custom URL file:
```
docker run -v /path/to/your/urls.txt:/app/urls.txt uptime-checker
```

## Endpoints

- `/metrics` - Prometheus metrics showing URL status and response times
- `/health` - Health check endpoint
- `/` - Returns OK

## Kubernetes

See `cronjob.yaml` for Kubernetes deployment (note: this will be updated to a Deployment once the web service is containerised).