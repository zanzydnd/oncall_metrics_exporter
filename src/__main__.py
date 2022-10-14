import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, Counter

from src.collectors import DaysWithoutUserOnCall, UsersWithoutTurnedOnNotificationsCollector
from src.config import settings, EXPORTER_API_REQUESTS_FAILED_TOTAL, EXPORTER_API_REQUESTS_TOTAL

if __name__ == "__main__":
    start_http_server(settings.ONCALL_EXPORTER_METRICS_PORT)
    REGISTRY.register(UsersWithoutTurnedOnNotificationsCollector())
    REGISTRY.register(DaysWithoutUserOnCall())
    while True:
        time.sleep(settings.ONCALL_EXPORTER_SCRAPE_INTERVAL)
