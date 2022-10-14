import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, Counter

from src.collectors import DaysWithoutUserOnCall, UsersWithoutTurnedOnNotificationsCollector
from src.config import settings, EXPORTER_API_REQUESTS_FAILED_TOTAL, EXPORTER_API_REQUESTS_TOTAL

if __name__ == "__main__":
    start_http_server(settings.ONCALL_EXPORTER_METRICS_PORT)
    REGISTRY.register(DaysWithoutUserOnCall())
    REGISTRY.register(UsersWithoutTurnedOnNotificationsCollector())
    REGISTRY.register(EXPORTER_API_REQUESTS_FAILED_TOTAL)
    REGISTRY.register(EXPORTER_API_REQUESTS_TOTAL)
    while True:
        time.sleep(settings.oncall_exporter_scrape_interval)
