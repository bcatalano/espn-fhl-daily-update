from config import *
from lib import *
from gmail import *

def main():
    # use url and credentials to get games and roster
    games_today     = getEvents(url_events, swid, espn_s2)
    roster          = getRoster(url, swid, espn_s2)

    # get relevant data from games and roster json files
    num_games       = getNumGames(games_today)
    game_info       = getGameInfo(games_today)
    teams_postponed = getPostponed(num_games, game_info)
    teams_playing   = getPlaying(num_games, game_info)
    not_playing     = getNotPlaying(roster, teams_postponed)
    active_out      = checkIfOut(roster, not_playing)
    benched_active  = getBenchedActive(roster, teams_playing, not_playing)
    [fc, dc, gc]    = getActivePlayerCount(roster, teams_playing, not_playing)

    # print information to text file
    printMessage(fc, dc, gc, not_playing, active_out, benched_active)

    # send an email to the user
    msg = readMessageFile()
    subject = "ESPN Fantasy Hockey Daily Roster Update"
    try:
        SendMessage(sender, to, subject, msg)
    except:
        SendMessage(sender, to, "[ERROR] - " + subject, "There was a problem sending the message, please try again later")

    return 0


if __name__ == "__main__":
    main()