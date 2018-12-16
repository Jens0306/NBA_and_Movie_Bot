import requests, json
from bs4 import BeautifulSoup
import re
import pandas as pd

def NBA_today():
    url = 'https://data.nba.net/10s/prod/v3/today.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)
    list = []
    list.append(reqsjson['seasonScheduleYear'])
    list.append(reqsjson['links']['currentDate'])
    return list
    
def NBA_team(year):
    url = 'https://data.nba.net/prod/v2/' + year + '/teams.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)

    list = []
    teams = reqsjson['league']['standard']
    for team in teams:
        if (team['isNBAFranchise']):
            if (team['nickname'].lower() == "76ers"):
                list.append(team['urlName'])
            else:
                list.append(team['nickname'].lower())
    # print(list)
    return list

def NBA_division(year):
    url = 'https://data.nba.net/prod/v2/' + year + '/teams.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)
    div = {
        "east": {
            "Atlantic",
            "Central",
            "Southeast"
        },
        "west": {
            "Southwest",
            "Northwest",
            "Pacific"
        }   
    }
    return div

def NBA_division_team(division, year):
    url = 'https://data.nba.net/prod/v2/' + year + '/teams.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)
    teams = reqsjson['league']['standard']
    data = {
        "Atlantic": [],
        "Central": [],
        "Southeast": [],
        "Southwest": [],
        "Northwest": [],
        "Pacific": []
    }
    for team in teams:
        if (team['isNBAFranchise']):
            if (team['nickname'] == "76ers"):
                data[team['divName']].append(team['urlName'])
            else:
                data[team['divName']].append(team['nickname'])
    print(data)
    return data[division]

def NBA_score(date):
    url = 'https://data.nba.net/prod/v2/' + date + '/scoreboard.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)

    games = reqsjson['games']
    scoreboard = "Games Today:\n--------------------------------\n"
    for content in games:
        # scoreboard += '      Q1 Q2 Q3 Q4\n'

        scoreboard += content['hTeam']['triCode'] + ' '
        # score each quarter
        # for score_quarter in content['hTeam']['linescore']:
            # scoreboard += score_quarter['score'] + ' '
        scoreboard += content['hTeam']['score'] + ' - '

        scoreboard += content['vTeam']['score'] + ' '
        scoreboard += content['vTeam']['triCode'] + '\n--------------------------------\n'
        # score each quarter
        # for score_quarter in content['vTeam']['linescore']:
            # scoreboard += score_quarter['score'] + ' '
    return scoreboard


def NBA_boxScore(date):
    url = 'https://data.nba.net/prod/v2/' + date + '/scoreboard.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)
    games = reqsjson['games']                  
    boxScore = "Box Score:\n--------------------------------\n"
    head = "https://watch.nba.com/game/" + date + "/"
    for content in games:
        teams = content['vTeam']['triCode'] + " vs. " + content['hTeam']['triCode']
        link = head + content['vTeam']['triCode'] + content['hTeam']['triCode'] + "#/boxscore"
        boxScore += teams + "\n" + link + "\n--------------------------------\n"
    return boxScore

def NBA_teamStats(team):
    url = requests.get("http://www.nba.com/" + team + "/stats/")
    soup = BeautifulSoup(url.content, "html.parser")
    stats = ['gp', 'pts', 'fgm', 'fg_pct', 'fg3_pct',
            'ft_pct', 'oreb', 'dreb', 'reb', 'ast',
            'stl', 'tov', 'pf', 'team']
    player_status = ""
    # getting all player names
    player_name = []
    player_data = soup.find_all("td")
    for i in range(0, len(player_data)//2, 14): # every 14th "td" tag in player_data contains player name
        player = str(player_data[i])
        idx_s = player.find('ank">') + 5
        idx_e = player.find('</a')
        player_name.append(player[idx_s:idx_e])

    # initializing data frame, filling with NaN's
    # df index = player name, columns = stat names
    df = pd.DataFrame(index=player_name, columns=stats)
    df.fillna(1)

    # parsing html document and assigning statistics to data frame
    # by row (player index). Finding player statistics via columns (statistic) was
    # not possible without information loss, due to the lack of html class attributed with 'td'
    # tags containing information for statistics with null values. For example, David Lee's lack of 3pt %
    # causes each data point for 3pt % to be shifted, because Lee's lack of data isn't recorded.
    player_index = 0
    for name in player_name:
        player_index += 1
        player_row = soup.find_all('tr')[player_index]
        player_status += name + ': '
        for stat in stats:
            stat_val = player_row.find('td', stat)
            df.at[name, stat] = stat_val # setting df value to html slice

            # handling missing values for stats.
            if df.loc[name, stat] == None:
                df.at[name, stat] = '-' # '-' used to signify lack of data, this will be coerced to NaN
            else:
                df.at[name, stat] = str(stat_val.contents[0]) # parse html slice to pull relevant statistic
                # removing %'s from pct stats
                if (stat == 'pts'):
                    ppg = int(df.loc[name, stat]) / float(df.loc[name, 'gp'])
                    # print(int(df.loc[name, stat]))
                    # print(int(df.loc[name, 'gp']))
                    player_status += str(round(ppg, 1)) + 'ppg\n'
                if '%' in df.loc[name ,stat]:
                    df.at[name, stat] = df.loc[name, stat].strip('%')

    # converting data type to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    # converting percentages to decimals in columns 3, 4, and 5
    df.iloc[:, 3] = round((df.iloc[:,3] / 100), 3)
    df.iloc[:, 4] = round((df.iloc[:,4] / 100), 3)
    df.iloc[:, 5] = round((df.iloc[:,5] / 100), 3)

    # adding team name to dataframe
    df.loc[:,'team'] = team

    # displaying data frame and ensuring all columns are visible
    pd.set_option('display.width', 1000)


    return player_status
    # return(df)

def NBA_standings():
    url = 'http://global.nba.com/statsm2/season/conferencestanding.json'
    rs = requests.session()
    res = rs.get(url, verify=True)
    reqsjson = json.loads(res.text)
    teamEast = reqsjson['payload']['standingGroups'][0]['teams']
    teamWest = reqsjson['payload']['standingGroups'][1]['teams']

    dictEast = {}
    dictWest = {}
    # listEast = []
    # listWest = []
    for team in teamEast:
        dictEast[team['profile']['name']] = team['standings']['confRank']
    listEast = sorted(dictEast, key=dictEast.__getitem__)
    text1 = "East\n----------------\n"
    for idx, team in enumerate(listEast):
        text1 += str(idx+1) + ". " + team + "\n"

    for team in teamWest:
        dictWest[team['profile']['name']] = team['standings']['confRank']
    listWest = sorted(dictWest, key=dictWest.__getitem__)
    text2 = "West\n----------------\n"
    for idx, team in enumerate(listWest):
        text2 += str(idx+1) + ". " + team + "\n"

    return [text1, text2]


def NBA_news():
    url = 'http://www.espn.com/nba/world-of-woj/'
    head = 'http://www.espn.com'
    print('Start parsing NBA news....')
    rs = requests.session()
    res = rs.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    content += "NBA NEWS:\n-------------------------------------------------\n"
    for index, data in enumerate(soup.select('.contentItem__content--story a'), 0):
        if index == 5:
            return content
        link = head + data['href']
        title = data.find('h1')
        title = title.text.strip()
        content += title + '\n' + link + '\n-------------------------------------------------\n'
        # print("===========================================================================")
        # print(title)
        # print("===========================================================================")
    # print(content)
    return content

def appleNews():
    targetURL = 'http://www.appledaily.com.tw/realtimenews/section/new/'
    head = 'http://www.appledaily.com.tw'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(targetURL, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 6:
            return content
        if head in data['href']:
            link = data['href']
        else:
            link = head + data['href']
        content += link + '\n----------------------------------\n'
    print(content)
    return content


