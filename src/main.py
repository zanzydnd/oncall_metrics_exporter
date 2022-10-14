# GET /api/v0/teams/{team}/rosters/{roster}/schedules - рассписания комманды
# GET /api/v0/teams/{team}/rosters/{roster}/users - люди в комманде
# GET /api/v0/teams/{team}/rosters/{roster} - Get user and schedule info for a roster
# GET /api/v0/teams/{team}/rosters - список ростеров
# GET /api/v0/teams/{team}/admins - список админов для комманды
# GET /api/v0/teams/{team}
# GET /api/v0/teams

# кол-во дней, когда у какой либо из команд нет человека. в течении сл 30 дней.
# кол-во комманд без slack
# кол-во л


import requests

# all_usernames = [user.get('name') for user in requests.get("http://localhost:8080/api/v0/users").json()]
#
# for user_name in all_usernames:
#     notifications_and_reminders = requests.get(f"http://localhost:8080/api/v0/users/{user_name}/notifications").json()
#     print(user_name)
from datetime import date, timedelta
from datetime import datetime

# today = datetime.combine(date.today(), datetime.min.time())
# past_30_days = today + timedelta(days=1)

# print(today.timestamp())
# print(past_30_days.timestamp())
# print(past_30_days.timestamp() - today.timestamp())
# print(datetime.fromtimestamp(1669618800))

st = {'asd','dsa'}
st.remove('c')