import logging
import os


class Config:
    ONCALL_EXPORTER_API_URL = os.environ.get("ONCALL_EXPORTER_API_URL")
    ONCALL_EXPORTER_SCRAPE_INTERVAL = os.environ.get("ONCALL_EXPORTER_SCRAPE_INTERVAL", 60)
    ONCALL_EXPORTER_LOG_LEVEL = os.environ.get("ONCALL_EXPORTER_LOG_LEVEL", logging.INFO)
    ONCALL_EXPORTER_METRICS_PORT = os.environ.get("ONCALL_EXPORTER_METRICS_PORT", 9091)


settings = Config()
