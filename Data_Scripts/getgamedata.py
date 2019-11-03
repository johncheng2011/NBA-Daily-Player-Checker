import mysql.connector

import database
import json,urllib.request
season = '2019-20'


data = urllib.request.urlopen("http://data.nba.net/data/10s/prod/v1/2019/schedule.json").read()
output = json.loads(data)


# for key in output['league']:
#     print(key)
# for key in output['league']['standard'][0]:
#     print(key)


mydb = database.connectDB(season)
mycursor = mydb.cursor()

# create table and add game data for each game
season = ''.join(season.split('-'))
mycursor.execute("CREATE TABLE IF NOT EXISTS games"+season+" (teamid INT, teamname VARCHAR(255),gamedate DATE, matchup VARCHAR (255), gameid INT, PRIMARY KEY (teamid,gameid))")

for game in output['league']['standard']:
    if(game['seasonStageId'] == 2):
        teamid1 = game['hTeam']['teamId']
        team1Abr = game['gameUrlCode'][-3:]
        teamid2 = game['vTeam']['teamId']
        team2Abr = game['gameUrlCode'][-6:-3]
        gamedate = game['startDateEastern'][:4] + '-' + game['startDateEastern'][4:6] + '-' + game['startDateEastern'][6:8]
        matchup = game['gameUrlCode'][-6:-3] + '@' + game['gameUrlCode'][-3:]
        gameid = game['gameId']



        sql = "INSERT INTO games"+ season +" (teamid,teamname,gamedate,matchup,gameid) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE teamid = %s"
        val = (teamid1,team1Abr,gamedate,matchup,gameid,teamid1)
        mycursor.execute(sql,val)
        val = (teamid2,team2Abr,gamedate,matchup,gameid,teamid2)
        mycursor.execute(sql,val)

mydb.commit()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)

