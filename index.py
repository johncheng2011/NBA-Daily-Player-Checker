from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, RadioField
from flask_wtf import FlaskForm
import mysql.connector
import json
from decimal import Decimal
from datetime import datetime, timedelta
from Data_Scripts import database
from flask_cors import CORS
import pandas as pd
import time
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'asdf3234bdfe'



class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def tomDate(date):
    dateObj = datetime.strptime(date,'%Y-%m-%d')
    dateObj += timedelta(days=1)
    dateStr = datetime.strftime(dateObj, '%Y-%m-%d')
    return dateStr
app.jinja_env.filters['tomorrowDate'] = tomDate

def yesDate(date):
    dateObj = datetime.strptime(date,'%Y-%m-%d')
    dateObj -= timedelta(days=1)
    dateStr = datetime.strftime(dateObj, '%Y-%m-%d')
    return dateStr
app.jinja_env.filters['yesterdayDate'] = yesDate


class date(FlaskForm):
    enterDate = DateField('dateInput',format = '%Y-%m-%d',default=datetime(2018,10,16))
    selectType = RadioField("Data Type", choices=[('1','per-game'),('2','zscores')],default='1')
    submit = SubmitField('submit')


@app.route("/", methods=['POST','GET'])
def index():
    form = date()
    if form.validate_on_submit():
        if(form.selectType.data == '1'):
            inDate = form.enterDate.data
            
            return redirect(url_for('players',date=inDate))
        else:
            return redirect(url_for('playerzscores',date=form.enterDate.data))
    return render_template('index.html',form = form,title="home")




@app.route("/games")
def games():
    return render_template('games.html')

@app.route("/all_players")
def all_players():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    players = []
    
    mycursor.execute('SELECT * FROM playerstats')
    players += mycursor.fetchall()
    
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return render_template('all_players.html',players=players)


@app.route("/all_players_zscores")
def all_playersz():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    players = []
    
    mycursor.execute('SELECT * FROM playerstatsz')
    players += mycursor.fetchall()
    
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return render_template('all_players_zscores.html',players=players)


@app.route("/players/<date>")
def players(date):
    
    return render_template('players.html',date=date)


@app.route("/players_zscores/<date>")
def playerzscores(date):
    
    return render_template('players_zscores.html',players=players,date=date)



@app.route("/_players/<date>")
def playerdata(date):
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        mycursor.execute('SELECT * FROM playerstats WHERE(teamid = '+ str(game[1]) +')')
        players += mycursor.fetchall()
    
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return json.dumps(players,cls=DecimalEncoder)

@app.route("/_players_zscores/<date>")
def getplayerszscores(date):
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        
        mycursor.execute('SELECT * FROM playerstatsz WHERE(teamid = '+ str(game[1]) +')')
        players += mycursor.fetchall()
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return json.dumps(players,cls=DecimalEncoder)

@app.route("/<player>")
def player_page(player):
    name,id = player.split('_')
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
)
    mycursor = db.cursor()
    sql = 'SELECT * FROM playergamelog WHERE(playerid=%s)'%(id)
    mycursor.execute(sql)
    desc = mycursor.description
    columns = [col[0] for col in desc]
    gamelog= [dict(zip(columns,row)) for row in mycursor]
    sql = 'SELECT * FROM playerstats WHERE(playerid=%s)'%(id)
    mycursor.execute(sql)
    desc = mycursor.description
    columns = [col[0] for col in desc]
    pergame= [dict(zip(columns,row)) for row in mycursor]
    pergame=pergame[0]
    sql = 'SELECT * FROM playerstatsz WHERE(playerid=%s)'%(id)
    mycursor.execute(sql)
    desc = mycursor.description
    columns = [col[0] for col in desc]
    zscore= [dict(zip(columns,row)) for row in mycursor]
    zscore=zscore[0]
    return render_template('player_page.html', gamelog=gamelog, pergame=pergame,zscore=zscore)

@app.route("/teams")
def teams():
    db = mysql.connector.connect(
    host =  database.databaseInfo["host"],
    user = database.databaseInfo["user"],
    passwd = database.databaseInfo["passwd"],
    database = database.databaseInfo["database"]
    )
    mycursor = db.cursor()
    teams = ['Atlanta_Hawks', 'Boston_Celtics', 'Brooklyn_Nets', 'Charlotte_Hornets', 'Chicago_Bulls', 'Cleveland_Cavaliers', 'Dallas_Mavericks', 'Denver_Nuggets', 'Detroit_Pistons', 'Golden_State_Warriors', 'Houston_Rockets', 'Indiana_Pacers', 'Los_Angeles_Clippers', 'Los_Angeles_Lakers', 'Menphis_Grizzlies', 'Miami_Heat', 'Milwaukee_Bucks', 'Minnesota_Timberwolves', 'New_Orleans_Pelicans', 'New_York_Knicks', 'Oklahoma_City_Thunder', 'Orlando_Magic', 'Philadelphia_76ers', 'Phoenix_Suns', 'Portland_Trail_Blazers', 'Sacramento_Kings', 'San_Antonio_Spurs', 'Toronto_Raptors', 'Utah_Jazz', 'Washington_Wizards']
    rosters = []
    players = {}
    for team in teams:
        sql = "SELECT * FROM " + team + "_Roster"
        mycursor.execute(sql)
        rosters = mycursor.fetchall()
        sql = "SELECT * FROM playerstats WHERE(teamid = " + str(rosters[0][0]) + ") ORDER BY pts DESC"
        mycursor.execute(sql)
        desc = mycursor.description
        columns = [col[0] for col in desc]
        players[team] = [dict(zip(columns,row)) for row in mycursor]

    return render_template('teams.html', rosters=players)
if __name__ == "__main__":
    app.run(host='0.0.0.0')

# playerstats
#{'playerid': 1628381, 'playername': 'John Collins', 'teamid': 1610612737, 'teamabbr': 'ATL', 'gp': 61, 'win': 24, 'loss': 37, 'min': Decimal('30.0'),
# 'fgm': Decimal('7.6'),'fga': Decimal('13.6'), 'fg_pct': Decimal('0.560'), 'fg3m': Decimal('0.9'), 'fg3a': Decimal('2.6'), 'fg3_pct': Decimal('0.348'), 
# 'ftm': Decimal('3.3'), 'fta': Decimal('4.4'), 'ft_pct': Decimal('0.763'), 'oreb': Decimal('3.6'), 'dreb': Decimal('6.2'), 'treb': Decimal('9.8'), 
# 'ast': Decimal('2.0'), 'stl': Decimal('0.4'), 'blk': Decimal('0.6'), 'pts': Decimal('19.5'), 'tov': Decimal('2.0'), 'fouls': Decimal('3.3')}

#playerstatsz
#{'playerid': 1629541, 'playername': 'Dairis Bertans', 'teamid': 1610612740, 'teamabbr': 'NOP', 'gp': 12, 'min': Decimal('13.9'), 
# 'fgz': Decimal('-1.59'), 'ftz': Decimal('-0.94'), 'fg3z': Decimal('-0.15'), 'rebz': Decimal('-1.16'), 'astz': Decimal('-0.67'), 
# 'stlz': Decimal('-1.27'), 'blkz': Decimal('-0.98'), 'ptsz': Decimal('-1.01'), 'tovz': Decimal('-1.11'), 'total': Decimal('-6.66')}

#playergamelog
#{'seasonid': 22018, 'playerid': 1629541, 'gameid': 21801215, 'gamedate': datetime.date(2019, 4, 9), 'matchup': 'NOP vs. GSW', 'win': 'L', 
# 'min': 26, 'fgm': 0, 'fga': 4, 'fg_pct': Decimal('0.000'), 'fg3m': 0, 'fg3a': 2, 'fg3_pct': Decimal('0.000'), 'ftm': 0, 'fta': 0, 
# 'ft_pct': Decimal('0.000'), 'oreb': 0, 'dreb': 0, 'reb': 0, 'ast': 2, 'stl': 0, 'blk': 0, 'tov': 0, 'pf': 1, 'pts': 0, 'plusminus': -7}

#games
#{'season': 22018, 'teamid': 1610612744, 'teamname': 'Golden State Warriors', 'gamedate': datetime.date(2019, 4, 10), 'matchup': 'GSW @ MEM', 'gameid': 21801225}