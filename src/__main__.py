import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from src.collectors import DaysWithoutUserOnCall, UsersWithoutTurnedOnNotificationsCollector
from src.config import settings

if __name__ == "__main__":
    start_http_server(settings.ONCALL_EXPORTER_METRICS_PORT)
    REGISTRY.register(DaysWithoutUserOnCall())
    REGISTRY.register(UsersWithoutTurnedOnNotificationsCollector())

    while True:
        time.sleep(settings.oncall_exporter_scrape_interval)
