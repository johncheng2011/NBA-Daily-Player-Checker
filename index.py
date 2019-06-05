from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, RadioField
from flask_wtf import Form 
import mysql.connector
import json
from decimal import Decimal


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf3234bdfe'

# db =  mysql.connector.connect(
#     host = 'localhost',
#     user = 'root',
#     passwd = 'gall2droyilx',
#     database = 'nbaplayers'
# )
# mycursor = db.cursor()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


title = "hello"
class date(Form):
    enterDate = DateField('dateInput',format = '%Y-%m-%d')
    selectType = RadioField("Data Type", choices=[('1','per-game'),('2','zscores')],default='1')
    submit = SubmitField('submit')


@app.route("/", methods=['POST','GET'])
def index():
    form = date()
    if form.validate_on_submit():
        if(form.selectType.data == '1'):
            return redirect(url_for('players',date=form.enterDate.data))
        else:
            return redirect(url_for('playerzscores',date=form.enterDate.data))
        #return url_for('players',title='games',form=form,games=games,players=players)
        #return redirect(url_for('test',date=form.enterDate.data))
        #return render_template('players.html',title="games",form=form,games=games,players=players)
    return render_template('index.html',form = form,title="home")






@app.route("/games")
def games():
    return render_template('games.html')
@app.route("/players/<date>")
def players(date):
    # mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    # games = mycursor.fetchall()
    # players = []
    # for game in games:
    #     #mycursor.execute('SELECT * FROM playerstatspergame WHERE(teamid = '+ str(game[1]) +')')
    #     mycursor.execute('SELECT * FROM playerstest WHERE(teamid = '+ str(game[1]) +')')
    #     players += mycursor.fetchall()
    # #return url_for('players',title='games',form=form,games=games,players=players)
    # players.sort(key = lambda x: x[1])
    return render_template('players.html',date=date)


@app.route("/players_zscores/<date>")
def playerzscores(date):
    # mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    # games = mycursor.fetchall()
    # players = []
    # for game in games:
    #     #mycursor.execute('SELECT * FROM playerstatspergame WHERE(teamid = '+ str(game[1]) +')')
    #     mycursor.execute('SELECT * FROM playerstatsz WHERE(teamid = '+ str(game[1]) +')')
    #     players += mycursor.fetchall()
    # #return url_for('players',title='games',form=form,games=games,players=players)
    # players.sort(key = lambda x: x[1])
    return render_template('players_zscores.html',title="players",players=players,date=date)
@app.route("/_players/<date>")
def playerdata(date):
    db =  mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'gall2droyilx',
    database = 'nbaplayers'
    )
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        mycursor.execute('SELECT * FROM playerstest WHERE(teamid = '+ str(game[1]) +')')
        players += mycursor.fetchall()
    #return url_for('players',title='games',form=form,games=games,players=players)
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return json.dumps(players,cls=DecimalEncoder)

@app.route("/_players_zscores/<date>")
def getplayerszscores(date):
    db =  mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'gall2droyilx',
    database = 'nbaplayers'
    )
    mycursor = db.cursor()
    mycursor.execute('SELECT * FROM games WHERE(gamedate = STR_TO_DATE("'+ str(date) +'","%Y-%m-%e")) ')
    games = mycursor.fetchall()
    players = []
    for game in games:
        #mycursor.execute('SELECT * FROM playerstatspergame WHERE(teamid = '+ str(game[1]) +')')
        mycursor.execute('SELECT * FROM playerstatsz WHERE(teamid = '+ str(game[1]) +')')
        players += mycursor.fetchall()
    #return url_for('players',title='games',form=form,games=games,players=players)
    db.disconnect()
    players.sort(key = lambda x: x[1])
    return json.dumps(players,cls=DecimalEncoder)

#"SELECT * FROM games WHERE (STR_TO_DATE(gamedate,'%Y-%m-%e') = STR_TO_DATE('".date("Y-m-d",strtotime($_POST['date']))."','%Y-%m-%e'))"
if __name__ == "__main__":
    app.run(host='0.0.0.0')