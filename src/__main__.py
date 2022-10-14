import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, Counter

from src.collectors import DaysWithoutUserOnCall, UsersWithoutTurnedOnNotificationsCollector
from src.config import settings

EXPORTER_API_REQUESTS_TOTAL = Counter("exporter_api_requests_total", "Total count of requests to oncall API")
EXPORTER_API_REQUESTS_FAILED_TOTAL = Counter(
    "exporter_api_requests_failed_total", "Total count of faled requests to oncall API")

if __name__ == "__main__":
    start_http_server(settings.ONCALL_EXPORTER_METRICS_PORT)
    REGISTRY.register(DaysWithoutUserOnCall())
    REGISTRY.register(UsersWithoutTurnedOnNotificationsCollector())

    while True:
        time.sleep(settings.oncall_exporter_scrape_interval)
