import requests

from prometheus_client.core import Gauge, GaugeMetricFamily
from datetime import date, timedelta
from datetime import datetime

from src.config import EXPORTER_API_REQUESTS_FAILED_TOTAL, EXPORTER_API_REQUESTS_TOTAL, EXPORTER_TIME_FOR_REQUEST
from src.config import settings


class UsersWithoutTurnedOnNotificationsCollector:
    """
        Класс, собирает метрику - кол-во юзеров, у которых не стоят никакие нотификации, когда они primary роль имеют.
    """

    def _count_users_without_turned_on(self) -> int:
        time_beg = datetime.now()
        users_response = requests.get(settings.ONCALL_EXPORTER_API_URL + "/api/v0/users")
        time_end = datetime.now()
        seconds = (time_end - time_beg).seconds
        EXPORTER_TIME_FOR_REQUEST.set(seconds)
        EXPORTER_API_REQUESTS_TOTAL.inc()
        if users_response.status_code != 200:
            EXPORTER_API_REQUESTS_FAILED_TOTAL.inc()
        all_usernames = [user.get('name') for user in users_response.json()]
        all_usernames_set = set(all_usernames)
        for user_name in all_usernames:
            EXPORTER_API_REQUESTS_TOTAL.inc()
            notifications_and_reminders_request = requests.get(
                settings.ONCALL_EXPORTER_API_URL + f"/api/v0/users/{user_name}/notifications")
            if notifications_and_reminders_request.status_code != 200:
                EXPORTER_API_REQUESTS_FAILED_TOTAL.inc()
            notifications_and_reminders = notifications_and_reminders_request.json()

            flag = False

            for notification in notifications_and_reminders:
                flag |= 'primary' in notification.get('roles')

            if flag:
                try:
                    all_usernames_set.remove(user_name)
                except KeyError:
                    pass

        return len(all_usernames_set)

    def collect(self):
        exporter_users_without_turned_on_gauge = GaugeMetricFamily(
            "exporter_users_without_turned_on_notification",
            "Check if we have users without turned on",
            labels=['exporter_users_without_turned_on']
        )
        exporter_users_without_turned_on_gauge.add_metric(['exporter_users_without_turned_on'],
                                                          self._count_users_without_turned_on())
        yield exporter_users_without_turned_on_gauge


class DaysWithoutUserOnCall:
    """
        Рассчитать кол-во дней, Когда ни у одной команды нет челвека на смене с ролью "primary" в течении сл 30 дней.
    """

    def _count_days_without_users_oncall(self):
        url_to_events = settings.ONCALL_EXPORTER_API_URL + "/api/v0/events"
        today = datetime.combine(date.today(), datetime.min.time())
        past_30_days = today + timedelta(days=30)
        all_dates_timestamps = set()
        for i in range(31):
            all_dates_timestamps.add((today + timedelta(days=i)).timestamp())
        url_all_teams = settings.ONCALL_EXPORTER_API_URL + "/api/v0/teams"

        EXPORTER_API_REQUESTS_TOTAL.inc()
        time_beg = datetime.now()
        team_names_response = requests.get(url_all_teams)
        time_end = datetime.now()
        seconds = (time_end - time_beg).seconds
        EXPORTER_TIME_FOR_REQUEST.set(seconds)
        if team_names_response.status_code != 200:
            EXPORTER_API_REQUESTS_FAILED_TOTAL.inc()

        for team_name in team_names_response.json():
            EXPORTER_API_REQUESTS_TOTAL.inc()
            response = requests.get(
                url_to_events,
                params={
                    "start__lt": int(past_30_days.timestamp()),
                    "end__ge": int(today.timestamp()),
                    "team__eq": team_name
                }
            )
            if response.status_code != 200:
                EXPORTER_API_REQUESTS_FAILED_TOTAL.inc()
            for record in response.json():
                if record.get('role') == "primary":
                    record_start_datetime = datetime.fromtimestamp(record.get('start'))
                    record_end_datetime = datetime.fromtimestamp(record.get('end'))
                    while record_start_datetime < record_end_datetime:
                        record_start_datetime = datetime.combine((record_start_datetime + timedelta(days=1)),
                                                                 datetime.min.time())
                        try:
                            all_dates_timestamps.remove(record_start_datetime.timestamp())
                        except KeyError:
                            pass

            return len(all_dates_timestamps)

    def collect(self):
        exporter_days_without_users_on_call_gauge = GaugeMetricFamily(
            "exporter_days_without_users_on_call",
            "Check if there are days in next 30 days without primary user on duty",
            labels=['exporter_days_without_users_on_call']
        )
        exporter_days_without_users_on_call_gauge.add_metric(['exporter_days_without_users_on_call'],
                                                             self._count_days_without_users_oncall())
        yield exporter_days_without_users_on_call_gauge
