import logging
import os

from prometheus_client.core import Counter, Gauge


class Config:
    ONCALL_EXPORTER_API_URL = os.environ.get("ONCALL_EXPORTER_API_URL", "http://localhost:8080")
    ONCALL_EXPORTER_SCRAPE_INTERVAL = os.environ.get("ONCALL_EXPORTER_SCRAPE_INTERVAL", 60)
    ONCALL_EXPORTER_LOG_LEVEL = os.environ.get("ONCALL_EXPORTER_LOG_LEVEL", logging.INFO)
    ONCALL_EXPORTER_METRICS_PORT = os.environ.get("ONCALL_EXPORTER_METRICS_PORT", 9091)


settings = Config()
EXPORTER_API_REQUESTS_TOTAL = Counter("exporter_api_requests_total", "Total count of requests to oncall API")
EXPORTER_API_REQUESTS_FAILED_TOTAL = Counter(
    "exporter_api_requests_failed_total", "Total count of faled requests to oncall API")

EXPORTER_TIME_FOR_REQUEST = Gauge(
    "exporter_time_for_request_in_seconds", "Time per One request in secons"
)
