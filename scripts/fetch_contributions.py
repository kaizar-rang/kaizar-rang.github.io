import json
import os
import urllib.request

TOKEN = os.environ["GH_TOKEN"]
LOGIN = "kaizar-rang"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
    headers={
        "Authorization": f"bearer {TOKEN}",
        "Content-Type": "application/json",
    },
)

with urllib.request.urlopen(req) as resp:
    payload = json.load(resp)

calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]

days = [
    {
        "date": day["date"],
        "count": day["contributionCount"],
        "level": LEVEL_MAP[day["contributionLevel"]],
    }
    for week in calendar["weeks"]
    for day in week["contributionDays"]
]

output = {
    "contributions": days,
    "total": {"lastYear": calendar["totalContributions"]},
}

with open("contributions.json", "w") as f:
    json.dump(output, f, indent=2)
    f.write("\n")
