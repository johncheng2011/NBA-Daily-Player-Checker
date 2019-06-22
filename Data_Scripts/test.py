import mysql.connector
import database
import itertools

db = mysql.connector.connect(
host =  database.databaseInfo["host"],
user = database.databaseInfo["user"],
passwd = database.databaseInfo["passwd"],
database = database.databaseInfo["database"]
)
mycursor = db.cursor()

mycursor.execute("SELECT * FROM games")
desc = mycursor.description
columns = [col[0] for col in desc]
players = [dict(zip(columns,row)) for row in mycursor]

for player in players:
    print(player)


# teams = ['Atlanta_Hawks', 'Boston_Celtics', 'Brooklyn_Nets', 'Charlotte_Hornets', 'Chicago_Bulls', 'Cleveland_Cavaliers', 'Dallas_Mavericks', 'Denver_Nuggets', 'Detroit_Pistons', 'Golden_State_Warriors', 'Houston_Rockets', 'Indiana_Pacers', 'Los_Angeles_Clippers', 'Los_Angeles_Lakers', 'Menphis_Grizzlies', 'Miami_Heat', 'Milwaukee_Bucks', 'Minnesota_Timberwolves', 'New_Orleans_Pelicans', 'New_York_Knicks', 'Oklahoma_City_Thunder', 'Orlando_Magic', 'Philadelphia_76ers', 'Phoenix_Suns', 'Portland_Trail_Blazers', 'Sacramento_Kings', 'San_Antonio_Spurs', 'Toronto_Raptors', 'Utah_Jazz', 'Washington_Wizards']
# rosters = []
# players = {}
# for team in teams:
#     sql = "SELECT * FROM " + team + "_Roster"
#     mycursor.execute(sql)
#     rosters = mycursor.fetchall()
#     sql = "SELECT * FROM playerstats WHERE(teamid = " + str(rosters[0][0]) + ") ORDER BY pts DESC"
#     mycursor.execute(sql)
#     desc = mycursor.description
#     columns = [col[0] for col in desc]

#     players[team] = [dict(zip(columns,row)) for row in mycursor]

# for player in players['Atlanta_Hawks']:
#     print(player)