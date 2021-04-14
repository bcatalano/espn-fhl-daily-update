import requests
from datetime import datetime
from pytz import timezone

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import os

import smtplib

def getEvents(url, swid, espn_s2):
    """Gets the games that are happening today.

    Args:
      url: ESPN api url.
      swid: personalized cookie credentials needed to access the api, you can find this in your browser.
      espn_s2: same as swid

    Returns:
      JSON object containing all information for games happening today.
    """
    r_events = requests.get(url, cookies={"swid" : swid,
                                          "espn_s2" : espn_s2})
    d_events = r_events.json()
    return d_events

def getRoster(url, swid, espn_s2):
    """Gets the team roster for today.

    Args:
      url: ESPN api url.
      swid: personalized cookie credentials needed to access the api, you can
            find this in your browser.
      espn_s2: same as swid

    Returns:
      List object containing roster information for today.
    """
    r = requests.get(url, cookies={"swid" : swid,
                                   "espn_s2" : espn_s2})
    d = r.json()
    roster = d['teams'][0]['roster']['entries']
    return roster

def getRosterSize(roster):
    """Gets the roster size.

    Args:
      roster: List object containing roster information.

    Returns:
      Length of the current roster.
    """
    return len(roster)

def getNumGames(d_events):
    """Gets the number of games that are happening today.

    Args:
      d_events: JSON object containing game information for today.

    Returns:
      Number of games ocurring today.
    """
    num_games = len(d_events['events'])
    return num_games

def getGameInfo(d_events):
    """Gets the games that are happening today.

    Args:
      d_events: JSON object containing game information.

    Returns:
      List object containing more useful information for games happening today.
    """
    game_info = d_events['events']
    return game_info

def getPostponed(num_games, game_info):
    """Gets teams that have postponed games for the day.

    Args:
      num_games: number of games happening today.
      game_info: list containing info for games happening today.

    Returns:
      List object containing team ids for postponed matchups.
    """
    teams_postponed = []
    for i in range(num_games):
        current_game = game_info[i]
        if (current_game['summary'] == "Postponed"):
            teams_postponed.append(int(current_game['competitors'][0]['id']))
            teams_postponed.append(int(current_game['competitors'][1]['id']))
    return teams_postponed

def getPlaying(num_games, game_info):
    """Gets the teams that are playing today.

    Args:
      num_games: number of games happening today.
      game_info: list containing info for games happening today.

    Returns:
      List object containing team ids for active matchups.
    """
    teams_playing = []
    for i in range(num_games):
        current_game = game_info[i]
        if (current_game['summary'] != "Postponed"):
            teams_playing.append(int(current_game['competitors'][0]['id']))
            teams_playing.append(int(current_game['competitors'][1]['id']))
    return teams_playing
    
def getNotPlaying(roster, teams_postponed):
    """Gets the teams that are playing today.

    Args:
      roster: list object containing roster information.
      teams_postponed: list containing teams that have postponed matchups.

    Returns:
      List object containing players that aren't playing due to injury, are out, or postponed.
    """
    not_playing = []
    for i in range(getRosterSize(roster)):
        currentPlayer = roster[i]['playerPoolEntry']['player']
        if(currentPlayer['injuryStatus'] in ['INJURY_RESERVE', 'OUT']):
            not_playing.append(currentPlayer['fullName'])
        elif (currentPlayer['proTeamId'] in teams_postponed):
            not_playing.append(currentPlayer['fullName'])
    return not_playing

def checkIfOut(roster, not_playing):
    """Checks if any players are out but not on bench.

    Args:
      roster: list object containing roster information.
      not_playing: list containing players that are not playing

    Returns:
      List object containing inactive players not on bench.
    """
    active_out = []
    for i in range(getRosterSize(roster)):
        currentPlayer = roster[i]['playerPoolEntry']['player']
        slotId = roster[i]['lineupSlotId']
        if ((currentPlayer['fullName'] in not_playing) and (slotId not in [7,8])):
            active_out.append(currentPlayer['fullName'])

    return active_out


def getBenchedActive(roster, teams_playing, not_playing):
    """Gets players that are benched but are playing today. Goalies will only be included if their starting status is "PROBABLE".

    Args:
      roster: list object containing roster information.
      teams_playing: list of teams that are playing today.
      not_playing: list containing players that are not playing.

    Returns:
      Dict object containing player names that are benched but will be playing and their player type (f, d, or g)
    """
    benched_active = {}
    for i in range(getRosterSize(roster)):
        currentPlayer = roster[i]['playerPoolEntry']['player']
        slotId = roster[i]['lineupSlotId']
        playerType = currentPlayer['defaultPositionId']
        if ((currentPlayer['proTeamId'] in teams_playing) and (slotId in [7,8]) and (currentPlayer['fullName'] not in not_playing)):
            if (playerType == 5):
                starter_status = list(currentPlayer['starterStatusByProGame'].values())[-1]
                if (starter_status == "PROBABLE"):
                    benched_active[currentPlayer['fullName']] = playerType
            else:
                benched_active[currentPlayer['fullName']] = playerType

    return benched_active

def getActivePlayerCount(roster, teams_playing, not_playing):
    """Gets number of active players by type.

    Args:
      roster: list object containing roster information.
      teams_playing: list of teams that are playing today.
      not_playing: list containing players that are not playing.

    Returns:
      3 item list object containing active forward, defenseman, and goalie count .
    """
    forwardCount = 0
    defenseCount = 0
    goalieCount = 0
    for i in range(getRosterSize(roster)):
        currentPlayer = roster[i]['playerPoolEntry']['player']
        slotId = roster[i]['lineupSlotId']
        playerType = currentPlayer['defaultPositionId']
        if ((currentPlayer['proTeamId'] in teams_playing) and (slotId not in [7,8]) and (currentPlayer['fullName'] not in not_playing)): 
            if(playerType in [1,2,3]):
                forwardCount += 1
            elif(playerType == 4):
                defenseCount += 1
            else:
                goalieCount += 1

    return [forwardCount, defenseCount, goalieCount]

def printMessage(fc, dc, gc, not_playing, active_out, benched_active):
    """Prints email message to text file in HTML format. 'message.txt' is created if it doesn't exist and overwritten everytime.

    Args:
      fc: active forward count.
      dc: active defensemen count.
      gc: active goalie count.
      not_playing: list of players not playing.
      active_out: list of out players in active spots.
      benched_active: list of benched players that are active today.

    Returns:
      Nothing.
    """
    message_file = open('message.txt', 'w+')
    tz = timezone('US/Eastern')
    todays_date = datetime.now(tz).strftime("%a %b %d")
    print('Here is your fantasy hockey roster update for ' + todays_date + '<br/>', file=message_file)

    if(len(benched_active) > 0):
        f_switch = False;
        d_switch = False;
        g_switch = False;
        for value in benched_active.values():
            if value in [1,2,3]:
                f_switch = True
            elif (value == 4):
                d_switch = True
            else:
                g_switch = True

        if (fc < 9 and f_switch):
            print('<b>[IMPORTANT]</b> You only have ' + str(fc) + '/9 active forwards set with active forwards on your bench!<br/>', file=message_file)
        if(dc < 5 and d_switch):
            print('<b>[IMPORTANT]</b> You only have ' + str(dc) + '/5 active defensemen set with active defensemen on your bench!<br/>', file=message_file)
        if(gc < 2 and g_switch):
            print('<b>[IMPORTANT]</b> You only have ' + str(gc) + '/2 active goalies set with probable starting goalies on your bench!<br/>', file=message_file)

        print('<br/>These are your benched active players:<br/>', file=message_file)
        for player in benched_active:
            print('- ' + player + '<br/>', file=message_file)
        print('<br/>', file=message_file)
    else:
        print('<br/><b>Your lineup looks good for today!</b><br/>', file=message_file)
   
    if (len(not_playing) > 0):
        print('<br/>Current Injuries/Players Out/PPD:<br/>', file=message_file)
        for player in not_playing:
            print('- ' + player + '<br/>', file=message_file)
        print('<br/>', file=message_file)

    if(len(active_out) > 0):
        print('Heads up, the following players are not playing and in your active lineup:<br/>', file=message_file)
        for player in active_out:
            print('- ' + player + '<br/>', file=message_file)
        print('<br/>', file=message_file)

    message_file.close()

def readMessageFile():
    """Reads email message from text file and removes \n characters.

    Args:
      None.

    Returns:
      String object containing HTML text to be included in email message.
    """
    with open('message.txt', 'r') as f:
        message_text = f.read().replace('\n','')
    f.close()
    return str(message_text)

def main():
    return


if __name__ == "__main__":
    main()