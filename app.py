from flask import *
from operator import itemgetter
from collections import OrderedDict
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
#socketio = SocketIO(app)

qbank = {
        '1' : ["What is 2 + 2?", [1, 4, 3, 5], "b"],
        '2' : ["What is the fifth root of 32?", [2, 4, 8, 16], "a"],
        '3' : ["What is the area of a 4x4 square?", [2, 8, 16, 12], "c"],
        '4' : ["Which country currently has the most cases of COVID-19?", ["USA", "China", "India", "Russia"], "a"],
        '5' : ["What is the fastest mile ever run by a human?", ["4:00", "3:52", "4:12", "3:43"], "d"],
        '6' : ["What is the largest planet in our solar system?", ["Mercuy", "Saturn", "Jupiter", "Earth"], "c"],
        '7' : ["Who is the current president of Russia?", ["Nikita Krushchev", "Vladimir Lenin", "Georgy Malenkov", "Vladimir Putin"], "d"],
        '8' : ["What is the national animal of Scotland?", ["Unicorn", "Golden Eagle", "Brown Bear", "Hog"], "a"],
        '9' : ["What is the most common letter in the English language?", ["E", "A", "I", "Y"], "a"],
        '10' : ["Who was the first president of the United States of America?", ["Barack Obama", "George Bush", "George Washington", "Bill Clinton"], "c"]}

regUsers = {}

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register', methods = ['POST'])
def register():
    user = request.form['fName']
    regUsers[user] = [0, 1]
    return getNextQuestion(user, '1', 0, getLeaderBoard())

@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    if request.method == 'POST':
        response = request.get_json()
        #print(response)
        username = response["uname"]
        qnum = response["qnum"]
        answer = response["answer"]
        updateUser(username, qnum, answer)
        lb = getLeaderBoard()

        #socketio.emit('leaderboard', jsonify(getLeaderBoard()), namespace = "/submit")
        #buf =  getNextQuestion(username, qnum + 1, regUsers[username][0])
        updateRes = {"uname":username, "qnum":qnum, "leaderboard":lb}
        #print(buf)
        return jsonify(updateRes)
    else:
        username = request.args.get("uname")
        qnum = int(request.args.get("qnum")) + 1
        lb = getLeaderBoard()
        if (qnum > len(qbank)):
            return render_template("congrats.html", user = username,
                                    score = regUsers[username][0])
        buf =  getNextQuestion(username, str(qnum), regUsers[username][0], lb)
        return buf

def getNextQuestion(uname, qn, score, lb):
    return render_template("questionpage.html", user = uname,
                points = score,
                qnum = qn,
                question = qbank[qn][0],
                choiceA = qbank[qn][1][0],
                choiceB = qbank[qn][1][1],
                choiceC = qbank[qn][1][2],
                choiceD = qbank[qn][1][3],
                leaderboard = lb
                )

def updateUser(uname, qn, choice):
    if (choice == qbank[str(qn)][2]):
        regUsers[uname][0] += 1
    regUsers[uname][1] += 1

def getLeaderBoard():
    scoreboard = {}
    for user in regUsers:
        scoreboard[user] = regUsers[user][0]
    leaderboard = OrderedDict(sorted(scoreboard.items(), key = itemgetter(1), reverse = True))
    #print(leaderboard)
    return leaderboard

if __name__ == '__main__':
   app.run(threaded = True, debug = True) #Insert ",host = 'your ip address', port = int('80')"
