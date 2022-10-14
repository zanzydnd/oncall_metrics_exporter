import requests

from prometheus_client.core import Gauge
from datetime import date, timedelta
from datetime import datetime


class UsersWithoutTurnedOnNotificationsCollector:
    """
        Класс, собирает метрику - кол-во юзеров, у которых не стоят никакие нотификации, когда они primary роль имеют.
    """

    def _count_users_without_turned_on(self) -> int:
        all_usernames = set([user.get('name') for user in requests.get("http://localhost:8080/api/v0/users").json()])

        for user_name in all_usernames:
            notifications_and_reminders = requests.get(
                f"http://localhost:8080/api/v0/users/{user_name}/notifications").json()

            flag = False

            for notification in notifications_and_reminders:
                flag |= 'primary' in notification.get('roles')

            if flag:
                all_usernames.remove(user_name)

        return len(all_usernames)

    def collect(self):
        exporter_users_without_turned_on_gauge = Gauge(
            "exporter_users_without_turned_on_notification",
            "Check if we have users without turned on"
        )
        exporter_users_without_turned_on_gauge.set(self._count_users_without_turned_on())
        yield exporter_users_without_turned_on_gauge


class DaysWithoutUserOnCall:

    def _count_days_without_users_oncall(self):
        # TODO: РАССЧИТАТЬ ВРЕМЯ!!!
        url_to_events = "http://127.0.0.1:8080/api/v0/events"
        today = datetime.combine(date.today(), datetime.min.time())
        past_30_days = today + timedelta(days=30)
        all_dates_timestamps = set()
        for i in range(31):
            all_dates_timestamps.add((today + timedelta(days=i)).timestamp())
        url_all_teams = "http://127.0.0.1:8080/api/v0/teams"

        team_names = requests.get(url_all_teams).json()

        for team_name in team_names:
            response = requests.get(
                url_to_events,
                params={
                    "end__ge": str(past_30_days.timestamp()),
                    "start__lt": str(today.timestamp()),
                    "team__eq": team_name
                }
            ).json()

            for record in response:
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
        exporter_days_without_users_on_call_gauge = Gauge(
            "exporter_users_without_turned_on_notification",
            "Check if we have users without turned on"
        )
        exporter_days_without_users_on_call_gauge.set(self._count_days_without_users_oncall())
        yield exporter_days_without_users_on_call_gauge
