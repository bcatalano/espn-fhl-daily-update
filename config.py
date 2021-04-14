from datetime import date

league_id = #<LEAGUE_ID>
year = #<YEAR>
team_id = #<TEAM_ID>

#url to get games occurring for today's date
date = str(date.today()).replace("-","")
url_events = "https://site.api.espn.com/apis/fantasy/v2/games/fhl/games?useMap=true&dates=" + date + "&pbpOnly=true"

# use the url that gives roster for the specific team
url = "https://fantasy.espn.com/apis/v3/games/fhl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id) + "?view=mRoster&forTeamId=" + str(team_id)

# use specific cookies as credentials to the private league
swid = #<SWID>
espn_s2 = #<ESPN_S2>

# sender and recipient of email notification message
sender = #<SENDER>
to = #<RECIPIENT>

def main():
    return


if __name__ == "__main__":
    main()
